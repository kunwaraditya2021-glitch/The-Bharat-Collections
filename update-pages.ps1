# PowerShell script to update remaining HTML pages with component system
# This script adds component-loader.js and replaces navbar/footer with placeholders

$pages = @("shop.html", "contact.html", "faq.html", "product-detail.html")
$templatesDir = "c:\Users\adity\Desktop\THE BHARAT COLLECTIONS\templates"

foreach ($page in $pages) {
    $filePath = Join-Path $templatesDir $page
    
    if (Test-Path $filePath) {
        Write-Host "Processing $page..."
        
        $content = Get-Content $filePath -Raw
        
        # Add component-loader.js script before </head>
        if ($content -notmatch "component-loader\.js") {
            $content = $content -replace '(\s*</head>)', "`n    <script src=`"/static/component-loader.js`"></script>`$1"
        }
        
        # Replace header section with navbar placeholder
        $content = $content -replace '(?s)(\s*<!-- .*?HEADER.*? -->.*?<header>.*?</header>)', "`n    <!-- Navbar Component Placeholder -->`n    <div id=`"navbar-placeholder`"></div>"
        
        # Replace footer section with footer placeholder  
        $content = $content -replace '(?s)(\s*<!-- .*?FOOTER.*? -->.*?<footer>.*?</footer>)', "`n    <!-- Footer Component Placeholder -->`n    <div id=`"footer-placeholder`"></div>"
        
        # Save the updated content
        Set-Content -Path $filePath -Value $content -NoNewline
        
        Write-Host "✓ Updated $page"
    } else {
        Write-Host "✗ File not found: $page"
    }
}

Write-Host "`nAll pages updated successfully!"
