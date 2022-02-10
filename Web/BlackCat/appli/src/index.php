<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8">
        <link href="assets/css/main.css" rel="stylesheet" type="text/css" />
        <script src="assets/js/index.js"></script>
        <script src="assets/js/polyfills.js"></script>
    </head>
    <body>
    <div id="sidenav" style="display: none;">
        <button id="sidenavBtn">&#9776;</button>
        <img id="profilePic" alt="An avatar that aims to represent the website owner" src="./img/avatar.png">
    </div>
    <div id="container">
        <div id="output"></div>
        <div id="input-line" class="input-line">
            <div id="prompt" class="prompt-color"></div>&nbsp;
            <div>
                <input type="text" id="cmdline" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
                    autofocus/>
            </div>
        </div>
    </div>
</body>
</html>