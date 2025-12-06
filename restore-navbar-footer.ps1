# PowerShell script to restore navbar and footer on all pages
# This reverts the component-based approach back to inline HTML

$pages = @("about.html", "shop.html", "contact.html", "faq.html", "product-detail.html")
$templatesDir = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates"

# Read the navbar and footer from index.html
$indexPath = Join-Path $templatesDir "index.html"
$indexContent = Get-Content $indexPath -Raw

# Extract navbar (from <header> to </header>)
$navbarPattern = '(?s)(\s*<!-- Header -->.*?</header>)'
if ($indexContent -match $navbarPattern) {
    $navbar = $matches[1]
    Write-Host "✓ Extracted navbar from index.html"
} else {
    Write-Host "✗ Could not extract navbar"
    exit
}

# Extract footer (from <!-- ===== FOOTER to </footer>)
$footerPattern = '(?s)(\s*<!-- ===== FOOTER.*?</footer>)'
if ($indexContent -match $footerPattern) {
    $footer = $matches[1]
    Write-Host "✓ Extracted footer from index.html"
} else {
    Write-Host "✗ Could not extract footer"
    exit
}

foreach ($page in $pages) {
    $filePath = Join-Path $templatesDir $page
    
    if (Test-Path $filePath) {
        Write-Host "`nProcessing $page..."
        
        $content = Get-Content $filePath -Raw
        
        # Remove component-loader script
        $content = $content -replace '\s*<script src="/static/component-loader\.js"></script>', ''
        
        # Replace navbar placeholder with actual navbar
        $content = $content -replace '(?s)\s*<!-- Navbar Component Placeholder -->.*?<div id="navbar-placeholder"></div>', $navbar
        
        # Replace footer placeholder with actual footer  
        $content = $content -replace '(?s)\s*<!-- Footer Component Placeholder -->.*?<div id="footer-placeholder"></div>', "`n$footer`n"
        
        # Save the updated content
        Set-Content -Path $filePath -Value $content -NoNewline
        
        Write-Host "✓ Updated $page"
    } else {
        Write-Host "✗ File not found: $page"
    }
}

Write-Host "`n✅ All pages restored successfully!"
Write-Host "Navbar and footer are now inline on all pages."
