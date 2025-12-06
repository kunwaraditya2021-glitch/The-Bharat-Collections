# Simple script to copy navbar and footer from index.html to other pages
$source = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates\index.html"
$pages = @("about.html", "shop.html", "contact.html", "faq.html", "product-detail.html")

# Read index.html
$indexHtml = Get-Content $source -Raw

# Extract navbar (lines 18-65)
$navbarStart = $indexHtml.IndexOf("    <!-- Header -->")
$navbarEnd = $indexHtml.IndexOf("    </header>") + "    </header>".Length
$navbar = $indexHtml.Substring($navbarStart, $navbarEnd - $navbarStart)

# Extract footer (from <!-- ===== FOOTER to </footer>)
$footerStart = $indexHtml.IndexOf("    <!-- ===== FOOTER")
$footerEnd = $indexHtml.IndexOf("    </footer>") + "    </footer>".Length  
$footer = $indexHtml.Substring($footerStart, $footerEnd - $footerStart)

Write-Host "Navbar length: $($navbar.Length)"
Write-Host "Footer length: $($footer.Length)"

foreach ($page in $pages) {
    $path = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates\$page"
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        
        # Remove component-loader script
        $content = $content -replace '<script src="/static/component-loader.js"></script>\r?\n', ''
        
        # Replace navbar placeholder
        $content = $content -replace '(?s)    <!-- Navbar Component Placeholder -->.*?    <div id="navbar-placeholder"></div>', $navbar
        
        # Replace footer placeholder
        $content = $content -replace '(?s)    <!-- Footer Component Placeholder -->.*?    <div id="footer-placeholder"></div>', $footer
        
        Set-Content $path -Value $content -NoNewline
        Write-Host "Updated: $page"
    }
}

Write-Host "Done!"
