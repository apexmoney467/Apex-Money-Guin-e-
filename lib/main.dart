import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(ApexApp());

class ApexApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Apex Money',
      theme: ThemeData(
        primaryColor: Color(0xFF008751), // Guinea Green
        scaffoldBackgroundColor: Colors.white,
        appBarTheme: AppBarTheme(backgroundColor: Color(0xFF008751)),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Color(0xFF008751),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))
          )
        )
      ),
      home: HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String balance = "0";
  String phone = "224622123456"; // CHANGE TO TEST NUMBER

  Future<void> getBalance() async {
    final url = Uri.parse("https://apex-money-guin-e.onrender.com/balance/$phone");
    final res = await http.get(url);
    setState(() {
      balance = json.decode(res.body)['balance'].toString();
    });
  }

  @override
  void initState() {
    super.initState();
    getBalance();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Apex Money')),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            // BALANCE CARD
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(30),
              decoration: BoxDecoration(
                color: Color(0xFF008751),
                borderRadius: BorderRadius.circular(20)
              ),
              child: Column(
                children: [
                  Text("Your Balance", style: TextStyle(color: Colors.white70, fontSize: 16)),
                  SizedBox(height: 10),
                  Text("$balance GNF", style: TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            SizedBox(height: 30),
            // BUTTONS
            ElevatedButton(
              onPressed: (){},
              child: Padding(
                padding: EdgeInsets.symmetric(vertical: 15, horizontal: 40),
                child: Text("Top Up", style: TextStyle(fontSize: 18))
              )
            ),
            SizedBox(height: 15),
            ElevatedButton(
              onPressed: (){},
              style: ElevatedButton.styleFrom(backgroundColor: Colors.grey[200], foregroundColor: Colors.black),
              child: Padding(
                padding: EdgeInsets.symmetric(vertical: 15, horizontal: 40),
                child: Text("Send Money", style: TextStyle(fontSize: 18))
              )
            ),
          ],
        ),
      ),
    );
  }
}
