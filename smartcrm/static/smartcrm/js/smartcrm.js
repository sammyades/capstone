// Run once when page loads
document.addEventListener('DOMContentLoaded', refreshDashboard);


// Auto-refresh every 60 seconds
setInterval(refreshDashboard, 60000);

async function refreshDashboard() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/dashboard-data/'); 
        
        // Check if the server returned a bad status code (like 404 or 500)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Update your dashboard DOM here
        if (document.getElementById('lead-count')) {
            document.getElementById('lead-count').textContent = data.lead_count;
            document.getElementById('deal-count').textContent = data.deal_count;
            document.getElementById('total-sales').textContent = `$${data.total_sales.toLocaleString()}`;
            document.getElementById('pending-tasks').textContent = data.pending_tasks;
        }
        
    } catch (error) {
        console.error("Failed to update dashboard:", error.message);
    }
}
        


// Lead form subission and lead list

const leadForm = document.querySelector('#lead-form');

if (leadForm) {
    leadForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Stop standard form submission page reload

        const formData = new FormData(this);
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        
        if (!csrfTokenElement) {
            console.error("CSRF token missing! Make sure {% csrf_token %} is inside your HTML form.");
            return;
        }

        try {
            
            const response = await fetch('/add_lead/', { 
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfTokenElement.value,
                }
            });

            if (response.ok) {
                window.location.href = '/lead/'; 
            } else {
                // Server validation failed
                const errorData = await response.json().catch(() => ({}));
                alert("Error saving lead. Please check the form data.");
                console.error("Server Error Response:", errorData);
            }
        } catch (error) {
            console.error("Network or server connection error:", error);
            alert("Network error. Please try again.");
        }
    });
}


function closeModal() {
    document.querySelector('#lead-modal').style.display = 'none';
}


// POST DATA: Creating a new note for a contact
async function addNote(leadId, noteText) {
    // Django requires the CSRF token for POST/PUT/DELETE
    const csrftoken = getCookie('csrftoken');

    const response = await fetch(`/api/contacts/${leadId}/notes/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ content: noteText })
    });

    if (response.ok) {
        console.log('Note saved!');
        loadContacts(); // Refresh list dynamically
    }
}

// Helper: Standard function to get Django's CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Covert Lead to Deal
document.addEventListener('DOMContentLoaded', function () {
    const convertForm = document.getElementById('convert-form');
    
    if (convertForm) {
        convertForm.addEventListener('submit', function (event) {
            const confirmConversion = confirm("Are you sure you want to convert this lead? This will create a new pipeline deal and attach all existing tasks to it.");
            
            if (!confirmConversion) {
                event.preventDefault();
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const statusForms = document.querySelectorAll('.status-form');
    
    statusForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            const response = confirm("Are you sure you want to change the pipeline status of this deal record?");
            if (!response) {
                event.preventDefault();
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const deleteForm = document.getElementById('delete-deal-form');
    
    if (deleteForm) {
        deleteForm.addEventListener('submit', function (event) {
            const finalConfirm = confirm("Are you absolutely sure you want to delete this deal? This action is permanent and will completely remove it from your pipeline tracking statistics.");
            
            if (!finalConfirm) {
                event.preventDefault(); // Blocks form submission if cancelled
            }
        });
    }
});

// Update Deal List
async function changeStatus(dealId, statusChoice) {
    try {
        // Construct the URL path to match your urls.py routing rule
        const response = await fetch(`/deal/${dealId}/status/${statusChoice}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'), // Required by Django for security
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Network response failed.');
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Success! Force reload the page content container or refresh layout smoothly
            window.location.reload(); 
        }
    } catch (error) {
        console.error('Error updating deal status status:', error);
    }
}

// Auto-dismiss flash alert messages 
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alertElement) {
        setTimeout(function () {
            // 
            try {
                if (window.bootstrap && window.bootstrap.Alert) {
                    const bsAlert = window.bootstrap.Alert.getOrCreateInstance(alertElement);
                    if (bsAlert) {
                        bsAlert.close();
                        return; // Exit if successful
                    }
                }
            } catch (e) {
                console.log("Bootstrap manual close backup triggered.");
            }

            // BULLETPROOF CSS FALLBACK (Runs if Bootstrap's class gets stuck)
            alertElement.style.transition = "all 0.5s ease";
            alertElement.style.opacity = "0";
            alertElement.style.transform = "translateY(-20px)"; // Adds a neat slide-up effect
            
            setTimeout(() => {
                alertElement.remove();
            }, 500);

        }, 4000); // 4 seconds
    });
});
