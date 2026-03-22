import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class AdminLoginDialog extends StatefulWidget {
  final String baseUrl;
  const AdminLoginDialog({super.key, required this.baseUrl});

  @override
  State<AdminLoginDialog> createState() => _AdminLoginDialogState();
}

class _AdminLoginDialogState extends State<AdminLoginDialog> {
  final _userCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  bool _isLoading = false;

  void _login() async {
    if (_userCtrl.text.isEmpty || _passCtrl.text.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final res = await http.post(
        Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/login/'),
        body: json.encode({'username': _userCtrl.text, 'password': _passCtrl.text})
      );
      if (res.statusCode == 200) {
        if (!mounted) return;
        Navigator.pop(context);
        Navigator.push(context, MaterialPageRoute(builder: (_) => AdminDashboardScreen(
           baseUrl: widget.baseUrl, username: _userCtrl.text, password: _passCtrl.text
        )));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hatalı giriş, sadece yetkililer.')));
      }
    } catch (_) {} finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: Colors.grey[900],
      title: const Text('Gizli CRM Girişi', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: _userCtrl, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Kullanıcı Adı', labelStyle: TextStyle(color: Colors.white54))),
          TextField(controller: _passCtrl, obscureText: true, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Şifre', labelStyle: TextStyle(color: Colors.white54))),
        ]
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('İptal')),
        ElevatedButton(
          style: ElevatedButton.styleFrom(backgroundColor: Colors.deepPurpleAccent),
          onPressed: _isLoading ? null : _login, 
          child: _isLoading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Text('Giriş Yap', style: TextStyle(color: Colors.white))
        ),
      ]
    );
  }
}

class AdminDashboardScreen extends StatefulWidget {
  final String baseUrl, username, password;
  const AdminDashboardScreen({super.key, required this.baseUrl, required this.username, required this.password});
  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  List _messages = [];
  bool _isLoading = true;
  bool _isFetchingMore = false;
  bool _hasNextPage = true;
  int _currentPage = 1;
  final Set<int> _selectedIds = {};
  
  String _searchQuery = "";
  Timer? _debounce;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _fetchMessages(refresh: true);
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200) {
        if (!_isLoading && !_isFetchingMore && _hasNextPage) {
          _fetchMessages();
        }
      }
    });
  }

  @override
  void dispose() {
    _debounce?.cancel();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _fetchMessages({bool refresh = false}) async {
    if (refresh) {
      if (mounted) setState(() { _isLoading = true; _currentPage = 1; _messages.clear(); _selectedIds.clear(); _hasNextPage = true; });
    } else {
      if (mounted) setState(() => _isFetchingMore = true);
    }
    
    try {
       final res = await http.post(
         Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/messages/'),
         body: json.encode({
           'username': widget.username, 
           'password': widget.password,
           'page': _currentPage,
           'search': _searchQuery
         })
       );
       if (res.statusCode == 200) {
         final decoded = json.decode(utf8.decode(res.bodyBytes));
         if (mounted) setState(() {
            _messages.addAll(decoded['messages']);
            _hasNextPage = decoded['has_next'] ?? false;
            if (_hasNextPage) _currentPage++;
         });
       }
    } catch (_) {} finally {
       if (mounted) setState(() { _isLoading = false; _isFetchingMore = false; });
    }
  }

  void _onSearchChanged(String val) {
    setState(() => _searchQuery = val);
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 600), () {
      _fetchMessages(refresh: true);
    });
  }

  void _showReplyDialog(Map msg) {
    final _replyCtrl = TextEditingController();
    bool _isReplying = false;
    showDialog(context: context, builder: (ctx) => StatefulBuilder(
      builder: (context, setStateDialog) => AlertDialog(
        backgroundColor: Colors.grey[900],
        title: Text('${msg['full_name']} Yanıtla', style: const TextStyle(color: Colors.white)),
        content: TextField(controller: _replyCtrl, maxLines: 3, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(hintText: 'Cevabınızı yazın... (Kişiye Push Bildirimi Olarak Gidecek)', hintStyle: TextStyle(color: Colors.white54))),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('İptal')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            onPressed: _isReplying ? null : () async {
              setStateDialog(() => _isReplying = true);
              try {
                await http.post(
                  Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/reply/'),
                  body: json.encode({'username': widget.username, 'password': widget.password, 'msg_id': msg['id'], 'reply_text': _replyCtrl.text})
                );
                if (mounted) { Navigator.pop(context); _fetchMessages(refresh: true); }
              } catch (_) {}
            }, 
            child: _isReplying ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator()) : const Text('Gönder ve Bildir', style: TextStyle(color: Colors.white))
          )
        ]
      )
    ));
  }

  void _showNotifyAllDialog() {
    final _titleCtrl = TextEditingController();
    final _msgCtrl = TextEditingController();
    bool _isSending = false;
    showDialog(context: context, builder: (ctx) => StatefulBuilder(
      builder: (context, setStateDialog) => AlertDialog(
        backgroundColor: Colors.grey[900],
        title: const Text('📢 Herkese Toplu Bildirim', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: _titleCtrl, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Başlık (Örn: Yeni Kampanya)')),
            TextField(controller: _msgCtrl, maxLines: 3, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Mesaj İçeriği')),
          ]
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('İptal')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
            onPressed: _isSending ? null : () async {
              setStateDialog(() => _isSending = true);
              try {
                final r = await http.post(
                  Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/notify_all/'),
                  body: json.encode({'username': widget.username, 'password': widget.password, 'title': _titleCtrl.text, 'message': _msgCtrl.text})
                );
                if (r.statusCode == 200 && mounted) {
                  Navigator.pop(context);
                  final count = json.decode(utf8.decode(r.bodyBytes))['count'] ?? 0;
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Toplu bildirim $count cihaza başarıyla gönderildi!')));
                }
              } catch (_) {} finally {
                setStateDialog(() => _isSending = false);
              }
            }, 
            child: _isSending ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator()) : const Text('Herkese Gönder', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold))
          )
        ]
      )
    ));
  }

  void _showNotifySelectedDialog() {
    final _titleCtrl = TextEditingController();
    final _msgCtrl = TextEditingController();
    bool _isSending = false;
    showDialog(context: context, builder: (ctx) => StatefulBuilder(
      builder: (context, setStateDialog) => AlertDialog(
        backgroundColor: Colors.grey[900],
        title: Text('🎯 ${_selectedIds.length} Kişiye Özel Bildirim', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: _titleCtrl, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Başlık')),
            TextField(controller: _msgCtrl, maxLines: 3, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Mesaj İçeriği')),
          ]
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('İptal')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
            onPressed: _isSending ? null : () async {
              setStateDialog(() => _isSending = true);
              try {
                final r = await http.post(
                  Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/notify_selected/'),
                  body: json.encode({'username': widget.username, 'password': widget.password, 'title': _titleCtrl.text, 'message': _msgCtrl.text, 'message_ids': _selectedIds.toList()})
                );
                if (r.statusCode == 200 && mounted) {
                  Navigator.pop(context);
                  setState(() => _selectedIds.clear());
                  final count = json.decode(utf8.decode(r.bodyBytes))['count'] ?? 0;
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Bildirim seçilen $count cihaza başarıyla gönderildi! (Kayıtsızlar hariç)')));
                }
              } catch (_) {} finally {
                setStateDialog(() => _isSending = false);
              }
            }, 
            child: _isSending ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator()) : const Text('Seçilenlere Gönder', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold))
          )
        ]
      )
    ));
  }

  void _deleteSelected() async {
     bool confirm = await showDialog(
       context: context,
       builder: (ctx) => AlertDialog(
         backgroundColor: Colors.grey[900],
         title: const Text('Emin misiniz?', style: TextStyle(color: Colors.white)),
         content: Text('${_selectedIds.length} adet mesajı silmek istiyor musunuz?', style: const TextStyle(color: Colors.white70)),
         actions: [
           TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('İptal')),
           ElevatedButton(
             style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
             onPressed: () => Navigator.pop(context, true), 
             child: const Text('Evet, Sil', style: TextStyle(color: Colors.white))
           ),
         ]
       )
     ) ?? false;

     if (!confirm) return;

     setState(() => _isLoading = true);
     try {
       await http.post(
         Uri.parse('${widget.baseUrl}/api/v1/mobile/admin/delete/'),
         body: json.encode({'username': widget.username, 'password': widget.password, 'message_ids': _selectedIds.toList()})
       );
       _fetchMessages(refresh: true);
     } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: _selectedIds.isNotEmpty 
          ? Text('${_selectedIds.length} Kişi Seçildi', style: const TextStyle(fontWeight: FontWeight.bold))
          : const Text('CRM Paneli', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: _selectedIds.isNotEmpty ? Colors.blueGrey[900] : Colors.deepPurple[900],
        leading: _selectedIds.isNotEmpty 
            ? IconButton(icon: const Icon(Icons.close), onPressed: () => setState(() => _selectedIds.clear())) 
            : null,
        actions: [
          if (_selectedIds.isNotEmpty)
            IconButton(icon: const Icon(Icons.delete, color: Colors.redAccent), onPressed: _deleteSelected),
          IconButton(icon: const Icon(Icons.refresh), onPressed: _fetchMessages),
        ]
      ),
      floatingActionButton: _selectedIds.isEmpty 
        ? FloatingActionButton.extended(
            onPressed: _showNotifyAllDialog,
            backgroundColor: Colors.redAccent,
            icon: const Icon(Icons.campaign, color: Colors.white),
            label: const Text('Toplu Bildirim', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold))
          )
        : FloatingActionButton.extended(
            onPressed: _showNotifySelectedDialog,
            backgroundColor: Colors.greenAccent[700],
            icon: const Icon(Icons.send_rounded, color: Colors.black),
            label: Text('${_selectedIds.length} Kişiye Gönder', style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold))
          ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              style: const TextStyle(color: Colors.white),
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.search, color: Colors.white54),
                hintText: 'Mesaj veya kişi ara...',
                hintStyle: const TextStyle(color: Colors.white54),
                filled: true,
                fillColor: Colors.grey[850],
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(vertical: 0)
              ),
            ),
          ),
          Expanded(
            child: _isLoading ? const Center(child: CircularProgressIndicator()) : ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
              itemCount: _messages.length,
              itemBuilder: (ctx, i) {
                final m = _messages[i];
                final replied = m['is_replied'] == true;
                final int msgId = m['id'];
                
                return Card(
                  color: Colors.grey[850],
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: _selectedIds.contains(msgId) ? const BorderSide(color: Colors.greenAccent, width: 2) : BorderSide.none
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(12),
                    leading: Checkbox(
                       value: _selectedIds.contains(msgId),
                       activeColor: Colors.greenAccent,
                       checkColor: Colors.black,
                       side: const BorderSide(color: Colors.white54),
                       onChanged: (bool? val) {
                          setState(() {
                             if (val == true) _selectedIds.add(msgId);
                             else _selectedIds.remove(msgId);
                          });
                       }
                    ),
                    title: Text('${m['full_name']} - ${m['subject']}', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                    subtitle: Padding(
                       padding: const EdgeInsets.only(top: 8),
                       child: Text('${m['message']}\n\n${m['created_at']}', style: const TextStyle(color: Colors.white70))
                    ),
                    trailing: replied 
                       ? const Text('Yanıtlandı', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold))
                       : ElevatedButton(
                           style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent, padding: const EdgeInsets.symmetric(horizontal: 12)),
                           onPressed: () => _showReplyDialog(m),
                           child: const Text('Yanıtla', style: TextStyle(color: Colors.white)),
                         ),
                    onTap: () {
                        setState(() {
                           if (_selectedIds.contains(msgId)) _selectedIds.remove(msgId);
                           else _selectedIds.add(msgId);
                        });
                    },
                  )
                );
              }
            ),
          ),
          if (_isFetchingMore)
             const Padding(padding: EdgeInsets.all(16.0), child: CircularProgressIndicator()),
        ],
      )
    );
  }
}
