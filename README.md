# Premier Research Club Website

A modern, responsive website for the Premier Research Club featuring glassmorphism design, smooth animations, and professional UI/UX.

## 🌐 Live Demo
**Website URL:** [Coming Soon - Will be added after GitHub Pages deployment]

## ✨ Features
- Modern glassmorphism design
- Responsive layout for all devices
- Smooth scroll animations
- Interactive particle background
- Timeline section
- Testimonials carousel
- Contact form
- Professional navigation with scroll effects

## 🚀 Quick Start

### Prerequisites
- **Visual Studio Code** (VS Code) - Download from https://code.visualstudio.com/
- **Live Server Extension** for VS Code
- Git (for deployment)

### Setting Up Live Server
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Live Server" by Ritwick Dey
4. Click "Install"
5. Restart VS Code

### Running the Website Locally
1. Open the project folder in VS Code (`J:\Github\RPC website`)
2. Right-click on `index.html` in the file explorer
3. Select "Open with Live Server"
4. Your website will automatically open in your browser at `http://127.0.0.1:5500`
5. Any changes you make will automatically refresh the browser!

## 📁 Project Structure

```
RPC website/
├── index.html          # Main HTML file - website structure
├── style.css           # CSS file - all styling and design
├── script.js           # JavaScript file - interactive functionality
└── assets/
    └── images/         # Folder for all images
        ├── README.md   # Guide for image requirements
        ├── logo.png    # Club logo (add your own)
        ├── hero-research.jpg
        ├── project images...
        └── team member photos...
```

## 🎨 Customizing Your Website

### 1. Changing Text Content

**Club Name and Tagline** (in `index.html`):
```html
<!-- Find this section in the hero -->
<h1 class="hero-title">
    Premier Research Club
    <span class="accent-text">Advancing Knowledge</span>
</h1>
<p class="hero-subtitle">
    Your new tagline goes here...
</p>
```

**Contact Information** (in `index.html`):
```html
<!-- Update these in the contact section -->
<p>info@yourclub.org</p>
<p>+1 (555) 123-4567</p>
<p>123 Your Address<br>Your City, State 12345</p>
```

### 2. Updating Colors and Styling

**Main Colors** (in `style.css`, at the top):
```css
:root {
    --primary-color: #2563eb;      /* Change this for main blue color */
    --accent-color: #f59e0b;       /* Change this for highlight color */
    --gray-900: #0f172a;          /* Dark text color */
}
```

**Popular Color Schemes:**
- **Academic Blue**: `--primary-color: #1e40af;`
- **Scientific Green**: `--primary-color: #059669;`
- **Medical Red**: `--primary-color: #dc2626;`
- **Tech Purple**: `--primary-color: #7c3aed;`

### 3. Adding/Editing Research Projects

**To Add a New Project** (in `index.html`):
1. Find the `<div class="projects-grid">` section
2. Copy an existing project card
3. Update the content:

```html
<div class="project-card">
    <div class="project-image">
        <img src="assets/images/your-project-image.jpg" alt="Your Project Name">
        <div class="project-overlay">
            <span class="project-status">Active</span>
        </div>
    </div>
    <div class="project-content">
        <h3 class="project-title">Your Project Title</h3>
        <p class="project-description">
            Your project description here...
        </p>
        <div class="project-tags">
            <span class="tag">Your Tag 1</span>
            <span class="tag">Your Tag 2</span>
        </div>
        <div class="project-footer">
            <div class="project-team">
                <img src="assets/images/team-member.jpg" alt="Researcher Name">
                <span>Dr. Researcher Name</span>
            </div>
            <button class="btn-learn-more">Learn More</button>
        </div>
    </div>
</div>
```

### 4. Adding Team Members

**Update Team Member Info**:
1. Add photos to `assets/images/` folder
2. Update project cards with new team member info
3. Keep photos at 150x150 pixels for consistency

### 5. Modifying Navigation

**To Add/Remove Menu Items** (in `index.html`):
```html
<ul class="nav-menu" id="nav-menu">
    <li class="nav-item">
        <a href="#home" class="nav-link">Home</a>
    </li>
    <li class="nav-item">
        <a href="#about" class="nav-link">About</a>
    </li>
    <!-- Add new menu item -->
    <li class="nav-item">
        <a href="#publications" class="nav-link">Publications</a>
    </li>
</ul>
```

## 🖼️ Managing Images

### Adding Images
1. Save images in the `assets/images/` folder
2. Use descriptive names: `malaria-research-project.jpg`
3. Optimize images for web (keep file sizes under 500KB)

### Image Requirements
- **Logo**: 40x40px, PNG with transparent background
- **Hero Images**: 800x500px minimum
- **Project Images**: 350x250px
- **Team Photos**: 150x150px (square)

### Getting Free Images
1. **Unsplash**: https://unsplash.com/ (free, high-quality)
2. **Pexels**: https://pexels.com/ (free stock photos)
3. **Pixabay**: https://pixabay.com/ (various free images)

Search terms: "research team", "laboratory", "healthcare", "technology", "education"

## 📱 Mobile Responsiveness

Your website is already mobile-friendly! It automatically adjusts to different screen sizes. Test it by:
1. Resizing your browser window
2. Using browser developer tools (F12 → Toggle device toolbar)
3. Testing on actual mobile devices

## 🔧 Common Modifications

### Adding a New Section
1. **HTML**: Add the section in `index.html`
```html
<section class="publications" id="publications">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">Publications</h2>
            <p class="section-subtitle">Our research publications and papers</p>
        </div>
        <!-- Your content here -->
    </div>
</section>
```

2. **CSS**: Add styling in `style.css`
```css
.publications {
    padding: var(--space-20) 0;
    background-color: var(--white);
}
```

3. **Navigation**: Add link to navigation menu

### Changing Fonts
**Using Google Fonts** (already included):
- Current fonts: Inter (body text) and Playfair Display (headings)
- To change: Update the Google Fonts link in `index.html` and font variables in `style.css`

### Form Integration
The contact form currently shows a demo. To make it functional:
1. **Backend**: Set up a server or use a service like Formspree, Netlify Forms, or EmailJS
2. **Update JavaScript**: Modify the `submitContactForm` function in `script.js`

Example with Formspree:
```javascript
// In script.js, replace the submitContactForm function
async submitContactForm(data) {
    const response = await fetch('https://formspree.io/f/your-form-id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    
    if (response.ok) {
        this.showSuccessMessage('Thank you! We\'ll get back to you soon.');
        this.contactForm.reset();
    } else {
        this.showErrorMessage('Sorry, there was an error. Please try again.');
    }
}
```

## 🌐 Publishing Your Website

### Option 1: GitHub Pages (Free)
1. Create a GitHub account
2. Create a new repository
3. Upload your files
4. Enable GitHub Pages in repository settings
5. Your site will be available at `https://yourusername.github.io/repository-name`

### Option 2: Netlify (Free)
1. Sign up at https://netlify.com
2. Drag and drop your project folder
3. Get instant hosting with automatic deployment

### Option 3: Traditional Web Hosting
1. Choose a hosting provider (Bluehost, SiteGround, etc.)
2. Upload files via FTP
3. Configure your domain

## 🌐 Deployment

### GitHub Pages (Recommended)
1. **Create a GitHub Repository:**
   - Go to [GitHub.com](https://github.com) and sign in
   - Click "New Repository"
   - Name it something like "premier-research-club" or "rpc-website"
   - Make it public
   - Don't initialize with README (we already have one)

2. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click "Settings" tab
   - Scroll down to "Pages" in the left sidebar
   - Under "Source", select "Deploy from a branch"
   - Select "main" branch and "/ (root)" folder
   - Click "Save"
   - Your website will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

### Alternative Deployment Options

#### Netlify
1. Go to [netlify.com](https://netlify.com)
2. Drag and drop your project folder
3. Get instant deployment with custom domain options

#### Vercel
1. Go to [vercel.com](https://vercel.com)
2. Connect your GitHub repository
3. Automatic deployments on every push

## 🔍 SEO and Performance Tips

### SEO Optimization
1. **Update Meta Tags** (in `index.html` `<head>` section):
```html
<title>Your Club Name - Advancing Research</title>
<meta name="description" content="Your club description for search engines">
```

2. **Add Alt Text** to all images:
```html
<img src="image.jpg" alt="Descriptive text about the image">
```

### Performance Tips
1. **Optimize Images**: Use tools like TinyPNG to compress images
2. **Minimize CSS/JS**: Use online minifiers before publishing
3. **Enable Caching**: Configure your web server for browser caching

## 🛠️ Troubleshooting

### Common Issues

**Website not loading in Live Server:**
- Make sure you have the Live Server extension installed
- Try restarting VS Code
- Check if another application is using port 5500

**Images not showing:**
- Check file paths are correct
- Ensure image files are in the `assets/images/` folder
- Verify image file names match what's in the HTML

**Mobile menu not working:**
- Check that JavaScript is loading (look for errors in browser console)
- Ensure all IDs match between HTML and JavaScript

**Styling looks wrong:**
- Check for typos in CSS class names
- Use browser developer tools (F12) to inspect elements
- Verify CSS file is linked correctly in HTML

### Browser Developer Tools
Press `F12` to open developer tools:
- **Console**: See JavaScript errors
- **Elements**: Inspect HTML and CSS
- **Network**: Check which files are loading
- **Device Toolbar**: Test mobile responsiveness

## 📚 Learning Resources

### HTML
- [MDN HTML Guide](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [W3Schools HTML Tutorial](https://www.w3schools.com/html/)

### CSS
- [MDN CSS Guide](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [CSS Tricks](https://css-tricks.com/)

### JavaScript
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)

### Design Inspiration
- [Dribbble](https://dribbble.com/) - Design inspiration
- [Behance](https://behance.net/) - Creative portfolios
- [Awwwards](https://awwwards.com/) - Award-winning websites

## 🆘 Getting Help

### Resources for Questions
1. **Stack Overflow**: Programming questions
2. **MDN Web Docs**: Official web development documentation
3. **CSS-Tricks**: CSS and design help
4. **VS Code Documentation**: Editor-specific help

### Code Comments
Your code includes extensive comments explaining:
- What each section does
- How to modify specific parts
- Best practices and accessibility considerations

Look for comments like:
```html
<!-- This section controls the navigation menu -->
```
```css
/* Main color palette - change these for different themes */
```
```javascript
// This function handles form submission
```

## 🎯 Next Steps

1. **Replace placeholder content** with your actual club information
2. **Add real images** following the specifications in `assets/images/README.md`
3. **Test on different devices** to ensure everything works properly
4. **Set up form processing** if you want the contact form to work
5. **Optimize for search engines** with proper meta tags and content
6. **Publish to the web** using one of the hosting options above

Remember: Start small, make one change at a time, and test frequently. The website is designed to be beginner-friendly, so don't be afraid to experiment!

Good luck with your Premier Research Club website! 🔬✨
