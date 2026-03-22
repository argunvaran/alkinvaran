import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:flutter/gestures.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';
import 'admin_panel.dart';
import 'dart:convert';
import 'dart:async';

void main() {
  runApp(const AlkinVaranApp());
}

final String _baseUrl = kIsWeb ? 'http://127.0.0.1:8000' : 'http://10.0.2.2:8000';

class AlkinVaranApp extends StatelessWidget {
  const AlkinVaranApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Alkin Varan',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.black,
        scaffoldBackgroundColor: const Color(0xFF121212),
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.grey,
          brightness: Brightness.dark,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blueAccent,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          )
        )
      ),
      scrollBehavior: const MaterialScrollBehavior().copyWith(
        dragDevices: {PointerDeviceKind.mouse, PointerDeviceKind.touch, PointerDeviceKind.stylus, PointerDeviceKind.unknown},
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  bool _isLoading = true;
  Map<String, dynamic> _data = {};
  String _errorMessage = '';
  
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _phoneController = TextEditingController();
  final _subjectController = TextEditingController();
  final _messageController = TextEditingController();
  bool _isSending = false;
  
  String? _deviceId;
  int _unreadCount = 0;

  @override
  void initState() {
    super.initState();
    _initDeviceId();
    _fetchData();
  }

  Future<void> _initDeviceId() async {
    final prefs = await SharedPreferences.getInstance();
    String? id = prefs.getString('device_id');
    if (id == null) {
      id = const Uuid().v4();
      await prefs.setString('device_id', id);
    }
    setState(() => _deviceId = id);
    _checkNotifications();
  }

  Future<void> _checkNotifications() async {
    if (_deviceId == null) return;
    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/notifications/?device_id=$_deviceId');
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final decoded = json.decode(utf8.decode(response.bodyBytes));
        if (decoded['success'] == true && mounted) {
           setState(() => _unreadCount = decoded['unread_count'] ?? 0);
        }
      }
    } catch (_) {}
  }

  Future<void> _fetchData() async {
    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/');
      final response = await http.get(url).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final decoded = json.decode(utf8.decode(response.bodyBytes));
        if (decoded['success'] == true) {
          setState(() {
            _data = decoded;
            _isLoading = false;
          });
        } else {
            setState(() {
              _errorMessage = decoded['error'] ?? 'API Hatası';
              _isLoading = false;
            });
        }
      } else {
        setState(() {
          _errorMessage = 'Sunucuya bağlanılamadı (Kod: ${response.statusCode})';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Bölümler yüklenirken hata oluştu. Sunucu bağlantınızı kontrol edin.';
        _isLoading = false;
      });
    }
  }

  Future<void> _submitContact() async {
    if (_nameController.text.isEmpty || _emailController.text.isEmpty || _messageController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Lütfen gerekli alanları doldurun.')));
      return;
    }
    setState(() => _isSending = true);
    
    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/contact/');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'full_name': _nameController.text,
          'email': _emailController.text,
          'phone': _phoneController.text,
          'subject': _subjectController.text,
          'message': _messageController.text,
          'device_id': _deviceId,
        })
      );

      if (response.statusCode == 200) {
         ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mesajınız başarıyla gönderildi!')));
         _nameController.clear();
         _emailController.clear();
         _phoneController.clear();
         _subjectController.clear();
         _messageController.clear();
      } else {
         ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Mesaj gönderilemedi.')));
      }
    } catch(e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Hata: $e')));
    } finally {
      setState(() => _isSending = false);
    }
  }

  void _openQuiz() {
    showDialog(context: context, builder: (context) => QuizDialog(deviceId: _deviceId));
  }

  void _openNotifications() {
     Navigator.push(context, MaterialPageRoute(builder: (_) => NotificationsScreen(deviceId: _deviceId))).then((_) {
        _checkNotifications();
     });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: GestureDetector(
          onLongPress: () {
            showDialog(context: context, builder: (context) => AdminLoginDialog(baseUrl: _baseUrl));
          },
          child: const Text('ALKIN VARAN', style: TextStyle(letterSpacing: 2.0, fontWeight: FontWeight.bold)),
        ),
        centerTitle: true,
        backgroundColor: Colors.black,
        elevation: 0,
        leading: IconButton(icon: const Icon(Icons.refresh), onPressed: () {
            setState(() { _isLoading = true; _errorMessage = ''; });
            _fetchData();
            _checkNotifications();
        }),
        actions: [
            IconButton(
               icon: Stack(
                 children: [
                    const Icon(Icons.notifications),
                    if (_unreadCount > 0)
                      Positioned(
                        right: 0,
                        top: 0,
                        child: Container(
                           padding: const EdgeInsets.all(2),
                           decoration: BoxDecoration(color: Colors.red, borderRadius: BorderRadius.circular(6)),
                           constraints: const BoxConstraints(minWidth: 12, minHeight: 12),
                           child: Text('$_unreadCount', style: const TextStyle(color: Colors.white, fontSize: 8, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                        )
                      )
                 ]
               ), 
               onPressed: _openNotifications
            ),
            const SizedBox(width: 8),
        ]
      ),
      body: _buildBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: () => launchUrl(Uri.parse('https://wa.me/905373973177'), mode: LaunchMode.externalApplication),
        backgroundColor: const Color(0xFF25D366),
        child: const Icon(Icons.chat_bubble, color: Colors.white, size: 28),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) return const Center(child: CircularProgressIndicator());
    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                    const Icon(Icons.error_outline, color: Colors.redAccent, size: 60),
                    const SizedBox(height: 16),
                    Text(_errorMessage, style: const TextStyle(color: Colors.redAccent), textAlign: TextAlign.center),
                ]
            )
        )
      );
    }
    
    final hero = _data['hero'] ?? {};
    final about = _data['about'] ?? {};
    final List studios = _data['studios'] ?? [];
    final List levels = _data['levels'] ?? [];
    final List disciplines = _data['disciplines'] ?? [];
    final List blogs = _data['blogs'] ?? [];

    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
            // Hero Section
            if (hero.isNotEmpty || hero.isEmpty) // Always show setup
              Container(
                padding: const EdgeInsets.symmetric(vertical: 60),
                decoration: BoxDecoration(
                  image: (hero.isNotEmpty && hero['background_image'] != null)
                    ? DecorationImage(
                        image: NetworkImage(hero['background_image']),
                        fit: BoxFit.cover,
                        colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.5), BlendMode.darken)
                      )
                    : null,
                  color: Colors.black, 
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Image.asset('assets/logo.png', height: 120), 
                      const SizedBox(height: 24),
                      Text(hero['title']?.replaceAll(RegExp(r'<[^>]*>'), '') ?? 'POTANSİYELİNİ ŞEKİLLENDİR', 
                        style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w900, color: Colors.white, height: 1.2),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 16),
                      Text(hero['subtitle']?.replaceAll(RegExp(r'<[^>]*>'), '') ?? 'Disiplin, hareket ve estetiğin mükemmel uyumuyla potansiyelinizi yeniden keşfedin.', 
                        style: const TextStyle(fontSize: 16, color: Colors.white70),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),

            // About Section
            if (about.isNotEmpty)
                Padding(
                    padding: const EdgeInsets.all(16).copyWith(top: 32),
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                            Text('HAKKIMDA', style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
                            const SizedBox(height: 8),
                            Text(about['title'] ?? '', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                            Text(about['highlight_title'] ?? '', style: const TextStyle(fontSize: 24, color: Colors.grey)),
                            const SizedBox(height: 16),
                            Text(about['content']?.replaceAll(RegExp(r'<[^>]*>'), '') ?? '', style: const TextStyle(fontSize: 16, height: 1.5)),
                        ]
                    )
                ),
            
            _buildSectionHeader('EĞİTİM SEVİYELERİ'),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: ElevatedButton.icon(
                onPressed: _openQuiz, 
                icon: const Icon(Icons.assignment), 
                label: const Text('Seviyeni Belirle (Teste Başla)', style: TextStyle(fontWeight: FontWeight.bold))
              ),
            ),
            _buildLevels(levels),

            _buildSectionHeader('DİSİPLİNLER'),
            _buildDisciplines(disciplines),
            
            _buildSectionHeader('STÜDYOLARIMIZ'),
            _buildStudios(studios),
            
            _buildSectionHeader('BLOG & YAZILAR'),
            BlogHorizontalList(blogs: blogs),

            _buildSectionHeader('İLETİŞİME GEÇ'),
            _buildContactForm(),
            
            const SizedBox(height: 80),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    if (title == 'BLOG & YAZILAR') {
      return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12).copyWith(top: 32),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 1.2)),
              TextButton(
                onPressed: () {
                   Navigator.push(context, MaterialPageRoute(builder: (_) => const BlogListScreen()));
                }, 
                child: const Text('Tümünü Gör', style: TextStyle(color: Colors.blueAccent))
              )
            ]
          )
      );
    }

    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12).copyWith(top: 32),
        child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: 1.2)),
    );
  }

  Widget _buildLevels(List levels) {
      if (levels.isEmpty) return const SizedBox.shrink();
      return ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: levels.length,
          itemBuilder: (context, index) {
              final level = levels[index];
              return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  color: Colors.grey[900],
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: ListTile(
                      leading: const Icon(Icons.fitness_center, color: Colors.blueAccent),
                      title: Text(level['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text(level['description'] ?? '', maxLines: 2, overflow: TextOverflow.ellipsis),
                  )
              );
          }
      );
  }

  Widget _buildDisciplines(List disciplines) {
      if (disciplines.isEmpty) return const SizedBox.shrink();
      return SizedBox(
          height: 220,
          child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 8),
              itemCount: disciplines.length,
              itemBuilder: (context, index) {
                  final disc = disciplines[index];
                  return Container(
                      width: 180,
                      margin: const EdgeInsets.symmetric(horizontal: 8),
                      decoration: BoxDecoration(
                          color: Colors.black45,
                          borderRadius: BorderRadius.circular(16),
                          image: disc['image'] != null 
                            ? DecorationImage(
                                image: NetworkImage(disc['image']),
                                fit: BoxFit.cover,
                                colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.5), BlendMode.darken)
                            )
                            : null,
                      ),
                      child: Center(
                          child: Padding(
                              padding: const EdgeInsets.all(12.0),
                              child: Text(
                                  disc['name'] ?? '',
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.white)
                              )
                          )
                      )
                  );
              }
          )
      );
  }

  Widget _buildStudios(List studios) {
      if (studios.isEmpty) return const SizedBox.shrink();
      return Column(
          children: studios.map((s) => Card(
              margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              color: Colors.grey[900],
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: InkWell(
                borderRadius: BorderRadius.circular(12),
                onTap: () {
                    final mapUrl = (s['map_link'] != null && s['map_link'].toString().isNotEmpty)
                        ? s['map_link']
                        : 'https://www.google.com/maps/search/Point+Athletics+İstanbul+Ümraniye+Hicret';
                    launchUrl(Uri.parse(mapUrl), mode: LaunchMode.externalApplication);
                },
                child: ListTile(
                    contentPadding: const EdgeInsets.all(12),
                    leading: s['image'] != null 
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.network(s['image'], width: 70, height: 70, fit: BoxFit.cover)
                          ) 
                        : const Icon(Icons.place, size: 40),
                    title: Text(s['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Padding(
                      padding: const EdgeInsets.only(top: 8.0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Icon(Icons.location_on, size: 16, color: Colors.blueAccent),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              (s['location'] != null && s['location'].toString().length > 15) 
                                  ? s['location'] 
                                  : 'İstanbul, Ümraniye, Mehmet Akif Mah., Hicret Sok., 12',
                              style: const TextStyle(height: 1.4, color: Colors.white70),
                            ),
                          ),
                        ],
                      ),
                    ),
                    trailing: const Icon(Icons.map, color: Colors.white30), 
                ),
              )
          )).toList()
      );
  }

  Widget _buildContactForm() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Card(
            color: Colors.grey[900],
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.camera_alt, color: Colors.blueAccent),
                  title: const Text('Instagram', style: TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: const Text('@alkinvaran'),
                  onTap: () => launchUrl(Uri.parse('https://www.instagram.com/alkinvaran')),
                ),
                const Divider(height: 1, color: Colors.white12),
                ListTile(
                  leading: const Icon(Icons.email, color: Colors.blueAccent),
                  title: const Text('E-posta', style: TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: const Text('alkinvaran@gmail.com'),
                  onTap: () => launchUrl(Uri.parse('mailto:alkinvaran@gmail.com')),
                ),
                const Divider(height: 1, color: Colors.white12),
                ListTile(
                  leading: const Icon(Icons.phone, color: Colors.blueAccent),
                  title: const Text('Telefon', style: TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: const Text('+90 537 397 31 77'),
                  onTap: () => launchUrl(Uri.parse('tel:+905373973177')),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Card(
            color: Colors.grey[900],
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text('DİREKT MESAJ', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white70)),
                  const SizedBox(height: 16),
                  TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'Adınız Soyadınız', border: OutlineInputBorder()),),
                  const SizedBox(height: 12),
                  TextField(controller: _emailController, decoration: const InputDecoration(labelText: 'E-posta', border: OutlineInputBorder()), keyboardType: TextInputType.emailAddress,),
                  const SizedBox(height: 12),
                  TextField(controller: _phoneController, decoration: const InputDecoration(labelText: 'Telefon', border: OutlineInputBorder()), keyboardType: TextInputType.phone,),
                  const SizedBox(height: 12),
                  TextField(controller: _subjectController, decoration: const InputDecoration(labelText: 'Konu', border: OutlineInputBorder()),),
                  const SizedBox(height: 12),
                  TextField(controller: _messageController, decoration: const InputDecoration(labelText: 'Mesajınız', border: OutlineInputBorder()), maxLines: 4,),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _isSending ? null : _submitContact,
                    child: _isSending ? const CircularProgressIndicator(color: Colors.white) : const Text('GÖNDER', style: TextStyle(fontWeight: FontWeight.bold)),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------- BLOG HORIZONTAL LIST (OK TUŞLU) ----------------

class BlogHorizontalList extends StatefulWidget {
  final List blogs;
  const BlogHorizontalList({super.key, required this.blogs});

  @override
  State<BlogHorizontalList> createState() => _BlogHorizontalListState();
}

class _BlogHorizontalListState extends State<BlogHorizontalList> {
  final ScrollController _scrollController = ScrollController();

  void _scrollLeft() {
    _scrollController.animateTo(
      (_scrollController.offset - 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  void _scrollRight() {
    _scrollController.animateTo(
      (_scrollController.offset + 300).clamp(0.0, _scrollController.position.maxScrollExtent),
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.blogs.isEmpty) return const SizedBox.shrink();
    return Stack(
      alignment: Alignment.center,
      children: [
        SizedBox(
            height: 260,
            child: ListView.builder(
                controller: _scrollController,
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 32), // Ok tuşlarına yer bırakmak için
                itemCount: widget.blogs.length,
                itemBuilder: (context, index) {
                    final blog = widget.blogs[index];
                    return Container(
                        width: 280,
                        margin: const EdgeInsets.symmetric(horizontal: 8),
                        child: Card(
                            color: Colors.grey[900],
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                            clipBehavior: Clip.antiAlias,
                            child: InkWell(
                              onTap: () {
                                 Navigator.push(context, MaterialPageRoute(builder: (_) => BlogDetailScreen(blogId: blog['id'], initialData: blog)));
                              },
                              child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.stretch,
                                  children: [
                                     Expanded(
                                       child: Image.network(
                                           blog['image'], 
                                           fit: BoxFit.cover,
                                           errorBuilder: (ctx, err, stack) => const Icon(Icons.broken_image, size: 50, color: Colors.white30)
                                       ),
                                     ),
                                     Padding(
                                        padding: const EdgeInsets.all(12.0),
                                        child: Column(
                                           crossAxisAlignment: CrossAxisAlignment.start,
                                           children: [
                                              Text(blog['title'] ?? '', maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                                              const SizedBox(height: 6),
                                              Text(blog['excerpt']?.replaceAll(RegExp(r'<[^>]*>'), '') ?? '', maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white54, fontSize: 13, height: 1.3)),
                                           ]
                                        )
                                     )
                                  ]
                              )
                            )
                        )
                    );
                }
            )
        ),
        Positioned(
          left: 8,
          child: CircleAvatar(
            backgroundColor: Colors.black.withOpacity(0.7),
            radius: 20,
            child: IconButton(
              icon: const Icon(Icons.chevron_left, color: Colors.white),
              onPressed: _scrollLeft,
              padding: EdgeInsets.zero,
            ),
          ),
        ),
        Positioned(
          right: 8,
          child: CircleAvatar(
            backgroundColor: Colors.black.withOpacity(0.7),
            radius: 20,
            child: IconButton(
              icon: const Icon(Icons.chevron_right, color: Colors.white),
              onPressed: _scrollRight,
              padding: EdgeInsets.zero,
            ),
          ),
        ),
      ],
    );
  }
}

// ---------------- BLOG LIST SCREEN (LAZY LOAD + ARAMA) ----------------

class BlogListScreen extends StatefulWidget {
  const BlogListScreen({super.key});

  @override
  State<BlogListScreen> createState() => _BlogListScreenState();
}

class _BlogListScreenState extends State<BlogListScreen> {
  final List _blogs = [];
  bool _isLoading = false;
  bool _hasNextPage = true;
  int _page = 1;
  String _searchQuery = '';
  
  final ScrollController _scrollController = ScrollController();
  Timer? _debounce;

  @override
  void initState() {
    super.initState();
    _fetchBlogs();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _debounce?.cancel();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200) {
      _fetchBlogs();
    }
  }

  void _onSearchChanged(String query) {
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () {
      if (_searchQuery != query) {
        setState(() {
          _searchQuery = query;
          _page = 1;
          _blogs.clear();
          _hasNextPage = true;
        });
        _fetchBlogs();
      }
    });
  }

  Future<void> _fetchBlogs() async {
    if (_isLoading || !_hasNextPage) return;

    setState(() => _isLoading = true);

    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/blogs/?page=$_page&q=$_searchQuery');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final decoded = json.decode(utf8.decode(response.bodyBytes));
        if (decoded['success'] == true) {
          setState(() {
            _page++;
            _hasNextPage = decoded['has_next'];
            _blogs.addAll(decoded['blogs']);
          });
        }
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Bağlantı hatası oluştu.')));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Makaleler ve Yazılar', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.black,
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            color: Colors.grey[900],
            child: TextField(
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: 'Yazılarda ara...',
                prefixIcon: const Icon(Icons.search, color: Colors.white54),
                filled: true,
                fillColor: Colors.black,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(vertical: 0)
              ),
            ),
          ),
          Expanded(
            child: _blogs.isEmpty && !_isLoading
                ? const Center(child: Text('Yazı bulunamadı.', style: TextStyle(color: Colors.white54)))
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _blogs.length + (_hasNextPage ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == _blogs.length) {
                        return const Padding(
                          padding: EdgeInsets.all(20),
                          child: Center(child: CircularProgressIndicator()),
                        );
                      }
                      
                      final blog = _blogs[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 16),
                        color: Colors.grey[900],
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        clipBehavior: Clip.antiAlias,
                        child: InkWell(
                          onTap: () {
                              Navigator.push(context, MaterialPageRoute(builder: (_) => BlogDetailScreen(blogId: blog['id'], initialData: blog)));
                          },
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Image.network(
                                blog['image'], 
                                height: 200, 
                                fit: BoxFit.cover,
                                errorBuilder: (_,__,___) => const SizedBox(height: 200, child: Icon(Icons.broken_image, size: 60, color: Colors.white30))
                              ),
                              Padding(
                                padding: const EdgeInsets.all(16),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(blog['title'] ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                                    const SizedBox(height: 6),
                                    Text(blog['excerpt'] ?? '', maxLines: 3, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white70, height: 1.4)),
                                    const SizedBox(height: 12),
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(blog['created_at'] ?? '', style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.w600, fontSize: 13)),
                                        const Text('Devamını Oku ->', style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold, fontSize: 13)),
                                      ],
                                    )
                                  ]
                                )
                              )
                            ]
                          )
                        )
                      );
                    },
                  )
          )
        ]
      )
    );
  }
}

// ---------------- BLOG DETAIL SCREEN ----------------

class BlogDetailScreen extends StatefulWidget {
  final int blogId;
  final Map<String, dynamic>? initialData;
  const BlogDetailScreen({super.key, required this.blogId, this.initialData});

  @override
  State<BlogDetailScreen> createState() => _BlogDetailScreenState();
}

class _BlogDetailScreenState extends State<BlogDetailScreen> {
  Map<String, dynamic>? _blogData;

  @override
  void initState() {
    super.initState();
    _blogData = widget.initialData;
    // content genelde excerpt olduğu için tamamı gerekiyorsa fetch yapılabilir.
    // _initialData if content is included in API: (Mobile API gönderiyor: 'content': b.content)
  }

  @override
  Widget build(BuildContext context) {
    if (_blogData == null) {
        return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
       appBar: AppBar(
          backgroundColor: Colors.black,
          elevation: 0,
       ),
       body: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
               Hero(
                  tag: 'blog_img_${_blogData!['id']}',
                  child: Image.network(
                    _blogData!['image'], 
                    height: 250, 
                    fit: BoxFit.cover,
                    errorBuilder: (_,__,___) => const SizedBox(height: 250, child: Icon(Icons.broken_image, size: 60, color: Colors.white30))
                  ),
               ),
               Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                       Text(_blogData!['created_at'] ?? '', style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.w600)),
                       const SizedBox(height: 8),
                       Text(_blogData!['title'] ?? '', style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold, height: 1.3)),
                       const SizedBox(height: 24),
                       // HTML renderer
                       Html(
                         data: _blogData!['content'] ?? '',
                         style: {
                            "body": Style(
                               color: Colors.white70,
                               fontSize: FontSize(16.0),
                               lineHeight: LineHeight.em(1.6),
                               margin: Margins.zero,
                               padding: HtmlPaddings.zero,
                            ),
                            "h1": Style(color: Colors.white, fontWeight: FontWeight.bold),
                            "h2": Style(color: Colors.white, fontWeight: FontWeight.bold),
                            "h3": Style(color: Colors.white, fontWeight: FontWeight.bold),
                            "a": Style(color: Colors.blueAccent, textDecoration: TextDecoration.underline),
                            "p": Style(margin: Margins.only(bottom: 12)),
                         },
                         onLinkTap: (url, _, __) {
                           if (url != null) launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
                         },
                       )
                    ]
                  )
               )
            ]
          )
       )
    );
  }
}

// ---------------- QUIZ WIDGET ----------------

class QuizDialog extends StatefulWidget {
  final String? deviceId;
  const QuizDialog({super.key, this.deviceId});

  @override
  State<QuizDialog> createState() => _QuizDialogState();
}

class _QuizDialogState extends State<QuizDialog> {
  int _currentStep = 1;
  int _score = 0;

  final _nameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();
  bool _isSending = false;

  void _answer(int points) {
    setState(() {
      _score += points;
      _currentStep++;
    });
  }

  String get _levelName {
    if (_score <= 5) return 'Temel Seviye';
    if (_score <= 9) return 'Orta Seviye';
    return 'İleri Seviye';
  }

  String get _levelDesc {
    if (_score <= 5) return 'Hareket dünyasına sağlam bir giriş yapmanız gerekiyor. Stabilite, mobilite ve core gücü eğitimleriyle temelleri korkusuzca atacağız.';
    if (_score <= 9) return 'Güzel bir altyapınız var. Amacımız artık dinamik kontroller, handstand denge sistemleri ve formları bir üst boyuta taşımak.';
    return 'Kondisyon ve farkındalığınız tepe noktada. Sınırları aşmak ve mükemmel teknik ile akrobatik formları inşa etmek için harika bir noktasınız.';
  }

  Future<void> _submitResult() async {
    if (_nameCtrl.text.isEmpty || _emailCtrl.text.isEmpty) return;
    setState(() => _isSending = true);
    
    final message = "Kişisel değerlendirme quiz'ini tamamladım.\n\nPuanım: $_score\nSeviyem: $_levelName";
    
    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/contact/');
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'full_name': _nameCtrl.text,
          'email': _emailCtrl.text,
          'phone': _phoneCtrl.text,
          'subject': 'Yeni Danışan Analizi: $_levelName',
          'message': message,
          'device_id': widget.deviceId,
        })
      );
      if (response.statusCode == 200 && mounted) {
        Navigator.pop(context); // close dialog
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Sonucunuz başarıyla gönderildi!')));
      }
    } catch(e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Hata: $e')));
    } finally {
      if (mounted) setState(() => _isSending = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.grey[900],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      insetPadding: const EdgeInsets.all(16),
      child: AnimatedSwitcher(duration: const Duration(milliseconds: 300), child: _buildContent()),
    );
  }

  Widget _buildContent() {
    if (_currentStep == 1) return _buildQuestion(1, 'Şu anki spor ve antrenman geçmişin nasıl?', [
      {'t': 'Spor geçmişim yok, yepyeni bir başlangıç yapmak istiyorum.', 'p': 1},
      {'t': 'Belli bir altyapım var, arada bir antrenman yapıyorum.', 'p': 2},
      {'t': 'Düzenli çalışıyorum, kontrol algım ve fitness kapasitem yüksek.', 'p': 4},
    ]);
    if (_currentStep == 2) return _buildQuestion(2, 'Handstand veya tumbling gibi formlara aşinalığın nedir?', [
      {'t': 'Kesinlikle hiç denemedim, nereden başlayacağımı bilmiyorum.', 'p': 1},
      {'t': 'Amuda kalkmayı vs. biraz denedim ama denge sağlayamıyorum.', 'p': 2},
      {'t': 'Temellerine fazlasıyla hakimim, rahat uygulayabiliyorum.', 'p': 4},
    ]);
    if (_currentStep == 3) return _buildQuestion(3, 'Bedenini değerlendirmek istersen en büyük eksikliğin ne tarafta?', [
      {'t': 'Esneklik sıfır, stabilite ve çekirdek gücüm yetersiz.', 'p': 1},
      {'t': 'Gücüm yerinde ama dinamik kontrol ve hareket geçişlerinde zorlanıyorum.', 'p': 2},
      {'t': 'Her şey ideal sayılır. Amacım artık sınırları kırıp mükemmeliyet!', 'p': 4},
    ]);

    return _buildResult();
  }
  
  Widget _buildResult() {
     return Padding(
      padding: const EdgeInsets.all(24.0),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.check_circle_outline, color: Colors.greenAccent, size: 60),
            const SizedBox(height: 16),
            const Text('Senin Seviyen:', style: TextStyle(fontSize: 18, color: Colors.grey)),
            Text(_levelName, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
            const SizedBox(height: 16),
            Text(_levelDesc, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70)),
            const SizedBox(height: 24),
            const Text('Detaylar için iletişime geçelim:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            TextField(controller: _nameCtrl, decoration: const InputDecoration(labelText: 'Ad Soyad', isDense: true)),
            const SizedBox(height: 8),
            TextField(controller: _emailCtrl, decoration: const InputDecoration(labelText: 'E-posta', isDense: true)),
            const SizedBox(height: 8),
            TextField(controller: _phoneCtrl, decoration: const InputDecoration(labelText: 'Telefon', isDense: true)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isSending ? null : _submitResult,
                child: _isSending ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white)) : const Text('Cevabımı Kendisine İlet', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Kapat', style: TextStyle(color: Colors.grey))),
          ],
        ),
      ),
    );
  }

  Widget _buildQuestion(int step, String qText, List<Map<String,dynamic>> options) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Soru $step / 3', style: const TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Text(qText, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, height: 1.3)),
          const SizedBox(height: 24),
          ...options.map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12.0),
            child: InkWell(
              onTap: () => _answer(opt['p']),
              borderRadius: BorderRadius.circular(12),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(border: Border.all(color: Colors.white24), borderRadius: BorderRadius.circular(12)),
                child: Text(opt['t'], style: const TextStyle(fontSize: 16)),
              ),
            ),
          )),
        ],
      ),
    );
  }
}

// ---------------- NOTIFICATIONS SCREEN ----------------

class NotificationsScreen extends StatefulWidget {
  final String? deviceId;
  const NotificationsScreen({super.key, required this.deviceId});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  List _notifications = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchNotifications();
  }

  Future<void> _fetchNotifications() async {
    if (widget.deviceId == null) {
      if (mounted) setState(() => _isLoading = false);
      return;
    }
    try {
      final url = Uri.parse('$_baseUrl/api/v1/mobile/notifications/?device_id=${widget.deviceId}');
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final decoded = json.decode(utf8.decode(response.bodyBytes));
        if (decoded['success'] == true && mounted) {
          setState(() => _notifications = decoded['notifications'] ?? []);
          _markAsRead();
        }
      }
    } catch (_) {} finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _markAsRead() async {
     try {
       await http.post(
         Uri.parse('$_baseUrl/api/v1/mobile/notifications/'),
         body: json.encode({'device_id': widget.deviceId}),
       );
     } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
       appBar: AppBar(
         title: const Text('Bildirimler', style: TextStyle(fontWeight: FontWeight.bold)),
         backgroundColor: Colors.black,
       ),
       body: _isLoading 
         ? const Center(child: CircularProgressIndicator())
         : _notifications.isEmpty
            ? const Center(child: Text('Henüz bir bildiriminiz bulunmuyor.', style: TextStyle(color: Colors.white54)))
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _notifications.length,
                itemBuilder: (context, index) {
                   final notif = _notifications[index];
                   return Card(
                     margin: const EdgeInsets.only(bottom: 12),
                     color: notif['is_read'] ? Colors.grey[900] : Colors.grey[850],
                     shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                     child: ListTile(
                       contentPadding: const EdgeInsets.all(16),
                       leading: CircleAvatar(
                         backgroundColor: notif['is_read'] ? Colors.black26 : Colors.blueAccent.withOpacity(0.2),
                         child: Icon(Icons.mark_email_unread, color: notif['is_read'] ? Colors.white54 : Colors.blueAccent),
                       ),
                       title: Text(notif['title'] ?? '', style: TextStyle(fontWeight: FontWeight.bold, color: notif['is_read'] ? Colors.white70 : Colors.white)),
                       subtitle: Column(
                         crossAxisAlignment: CrossAxisAlignment.start,
                         children: [
                           const SizedBox(height: 8),
                           Text(notif['message'] ?? '', style: const TextStyle(color: Colors.white70)),
                           const SizedBox(height: 8),
                           Text(notif['created_at'] ?? '', style: const TextStyle(fontSize: 12, color: Colors.white30)),
                         ],
                       ),
                     ),
                   );
                },
            )
    );
  }
}
