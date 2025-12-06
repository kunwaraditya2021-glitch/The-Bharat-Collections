# PowerShell script to fix about.html navbar and footer
$indexPath = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates\index.html"
$aboutPath = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates\about.html"

# Read both files
$indexContent = Get-Content $indexPath -Raw
$aboutContent = Get-Content $aboutPath -Raw

# Extract navbar from index.html (from <body> to </header>)
$navbarStart = $indexContent.IndexOf("<body>")
$navbarEnd = $indexContent.IndexOf("</header>") + "</header>".Length
$navbar = $indexContent.Substring($navbarStart, $navbarEnd - $navbarStart)

# Extract footer from index.html (from <!-- ===== FOOTER to </footer>)
$footerStart = $indexContent.IndexOf("<!-- ===== FOOTER")
$footerEnd = $indexContent.IndexOf("</footer>") + "</footer>".Length  
$footer = $indexContent.Substring($footerStart, $footerEnd - $footerStart)

Write-Host "Navbar extracted: $($navbar.Length) characters"
Write-Host "Footer extracted: $($footer.Length) characters"

# Replace navbar in about.html
$aboutNavbarStart = $aboutContent.IndexOf("<body>")
$aboutNavbarEnd = $aboutContent.IndexOf("</header>") + "</header>".Length
$aboutContent = $aboutContent.Substring(0, $aboutNavbarStart) + $navbar + $aboutContent.Substring($aboutNavbarEnd)

# Replace footer in about.html
$aboutFooterStart = $aboutContent.IndexOf("<!-- ===== FOOTER")
$aboutFooterEnd = $aboutContent.IndexOf("</footer>") + "</footer>".Length
$aboutContent = $aboutContent.Substring(0, $aboutFooterStart) + $footer + $aboutContent.Substring($aboutFooterEnd)

# Save the updated about.html
Set-Content $aboutPath -Value $aboutContent -NoNewline

Write-Host "✅ about.html updated successfully!"
