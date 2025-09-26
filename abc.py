<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EduCoin Classroom Crypto</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>💰 EduCoin: Classroom Crypto</h1>

  <section id="teacher">
    <h2>Teacher Panel</h2>
    <select id="studentSelect"></select>
    <button onclick="mintCoin()">Mint 1 Coin</button>
  </section>

  <section id="student">
    <h2>Student Panel</h2>
    <label for="wallet">Your Wallet:</label>
    <select id="wallet" onchange="updateBalanceAndLeaderboard()"></select>

    <p>Your Balance: <span id="balance">0</span> EDC</p>

    <h3>Transfer Coins</h3>
    <label for="recipient">To:</label>
    <select id="recipient"></select>

    <label for="amount">Amount:</label>
    <input type="number" id="amount" min="1" value="1">
    <button onclick="transfer()">Send</button>
  </section>

  <section>
    <h2>🏆 Leaderboard</h2>
    <ol id="leaderboard"></ol>
  </section>

  <script src="script.js"></script>
</body>
</html>
