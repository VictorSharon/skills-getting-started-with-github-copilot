document.addEventListener('DOMContentLoaded', () => {
  loadActivities();
  setupFormHandler();
});

async function loadActivities() {
  try {
    const response = await fetch('/activities?cache=' + Date.now());
    const activities = await response.json();
    
    displayActivities(activities);
    populateActivityDropdown(activities);
  } catch (error) {
    console.error('Error loading activities:', error);
    document.getElementById('activities-list').innerHTML = '<p>Error loading activities.</p>';
  }
}

function displayActivities(activities) {
  const container = document.getElementById('activities-list');
  container.innerHTML = '';
  
  Object.entries(activities).forEach(([name, details]) => {
    const card = document.createElement('div');
    card.className = 'activity-card';
    
    const participantCount = details.participants.length;
    const spotsAvailable = details.max_participants - participantCount;
    
    card.innerHTML = `
      <h4>${name}</h4>
      <p><strong>Description:</strong> ${details.description}</p>
      <p><strong>Schedule:</strong> ${details.schedule}</p>
      <p><strong>Spots Available:</strong> ${spotsAvailable}/${details.max_participants}</p>
      <div class="participants-section">
        <strong>Participants (${participantCount}):</strong>
        <ul class="participants-list">
          ${details.participants.length > 0 
            ? details.participants.map(email => `<li><span>${email}</span> <button class="delete-btn" data-activity="${name}" data-email="${email}" title="Unregister">×</button></li>`).join('')
            : '<li class="no-participants">No participants yet</li>'}
        </ul>
      </div>
    `;
    
    container.appendChild(card);
  });
  
  // Attach delete button listeners
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const activity = btn.dataset.activity;
      const email = btn.dataset.email;
      await unregisterFromActivity(activity, email);
    });
  });
}

function populateActivityDropdown(activities) {
  const signupSelect = document.getElementById('activity');

  if (!signupSelect) return;
  // Remove existing non-placeholder options
  Array.from(signupSelect.querySelectorAll('option')).forEach(o => {
    if (o.value !== '') o.remove();
  });
  Object.keys(activities).forEach(name => {
    const option = document.createElement('option');
    option.value = name;
    option.textContent = name;
    signupSelect.appendChild(option);
  });
}

function setupFormHandler() {
  document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const activity = document.getElementById('activity').value;
    const messageDiv = document.getElementById('message');
    
    if (!activity) {
      showMessage('Please select an activity', 'error');
      return;
    }
    
    try {
      const response = await fetch(`/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const result = await response.json();
        showMessage(result.message, 'success');
        document.getElementById('signup-form').reset();
        loadActivities();
      } else {
        const error = await response.json();
        showMessage(error.detail, 'error');
      }
    } catch (error) {
      showMessage('Error signing up for activity', 'error');
    }
  });
}

function showMessage(text, type) {
  const messageDiv = document.getElementById('message');
  messageDiv.textContent = text;
  messageDiv.className = `message ${type}`;
}

async function unregisterFromActivity(activity, email) {
  try {
    const response = await fetch(`/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`, {
      method: 'POST'
    });

    if (response.ok) {
      const result = await response.json();
      showMessage(result.message, 'success');
      loadActivities();
    } else {
      const error = await response.json();
      showMessage(error.detail, 'error');
    }
  } catch (error) {
    showMessage('Error unregistering from activity', 'error');
  }
}
