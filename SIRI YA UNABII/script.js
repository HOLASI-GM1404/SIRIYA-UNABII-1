// Track views and downloads
let bookViews = {
    'alama-ya-mnyama': 0,
    'wafu-wako-wapi': 0,
    'nyimbo-za-krisito-sda': 0,
    'roho-mtakatifu': 0,
    'mpango-wa-usomaji-biblia': 0,
    'siku-10-za-maombi': 0,
    'juma-la-maombi': 0
};

// Load views from localStorage
function loadViews() {
    const savedViews = localStorage.getItem('bookViews');
    if (savedViews) {
        bookViews = JSON.parse(savedViews);
        updateViewCounters();
    }
}

// Save views to localStorage
function saveViews() {
    localStorage.setItem('bookViews', JSON.stringify(bookViews));
}

// Update view counters on the page
function updateViewCounters() {
    for (const bookId in bookViews) {
        const counterElement = document.getElementById(`views-${bookId}`);
        if (counterElement) {
            counterElement.textContent = bookViews[bookId];
        }
    }
}

// Track a view
function trackView(bookId) {
    // Show the book content (in a real app, this would display the book)
    alert(`Kitabu "${getBookTitle(bookId)}" kinaonyeshwa.`);
    
    // Increment view count
    bookViews[bookId]++;
    document.getElementById(`views-${bookId}`).textContent = bookViews[bookId];
    saveViews();
    
    // In a real app, you would send this data to your server
    // sendViewData(bookId);
}

// Track a download
function trackDownload(bookId) {
    // Increment view count (counting downloads as views too)
    bookViews[bookId]++;
    document.getElementById(`views-${bookId}`).textContent = bookViews[bookId];
    saveViews();
    
    // In a real app, you would send this data to your server
    // sendDownloadData(bookId);
}

// Helper function to get book title from ID
function getBookTitle(bookId) {
    const titles = {
        'alama-ya-mnyama': 'Alama Ya Mnyama',
        'wafu-wako-wapi': 'Wafu Wako Wapi',
        'nyimbo-za-krisito-sda': 'Nyimbo Za Krisito SDA',
        'roho-mtakatifu': 'Roho Mtakatifu',
        'mpango-wa-usomaji-biblia': 'Mpango Wa Usomaji Biblia Kwa Mwaka',
        'siku-10-za-maombi': 'Siku 10 Za Maombi 2023 Kurejea Madhabahuni',
        'juma-la-maombi': 'Juma La Maombi – November 2022 Wanafunzi Wanaokua'
    };
    return titles[bookId] || bookId;
}

// Handle contact form submission
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    
    // In a real app, you would send this data to your server
    // sendContactForm(name, email, subject, message);
    
    alert('Asante kwa ujumbe wako! Tutawasiliana nawe hivi karibuni.');
    this.reset();
});

// Smooth scrolling for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetElement.offsetTop - 80,
            behavior: 'smooth'
        });
    });
});

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadViews();
    
    // Add animation to book cards when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.book-card').forEach(card => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});

// In a real implementation, you would have functions to send data to your server
/*
function sendViewData(bookId) {
    fetch('/api/track-view', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ bookId }),
    });
}

function sendDownloadData(bookId) {
    fetch('/api/track-download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ bookId }),
    });
}

function sendContactForm(name, email, subject, message) {
    fetch('/api/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, subject, message }),
    });
}
*/
// YouTube API integration
function loadYouTubeVideos() {
    // Implement YouTube API integration
}

window.onload = () => {renderBooks();
    loadYouTubeVideos();};

    etElementById('subscribe-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const emailInput = document.getElementById('email');
        const messageEl = document.getElementById('subscribe-message');
        const email = emailInput.value;
      
        fetch('/subscribe', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            messageEl.style.color = 'green';
            messageEl.textContent =  'Thank you for subscribing!';
            emailInput.value = '';
          } else {
            messageEl.style.color = 'red';
            messageEl.textContent = 'Error: ' + data.message;
          }
        })
        .catch(error => {
          messageEl.style.color = 'red';
          messageEl.textContent = 'An error occurred. Please try again.';
          console.error('Error:', error);
        });
      });  