function toggleMenu() {
    var menu = document.getElementById("dropdown-menu");
    menu.classList.toggle("show");
}

// Close dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.user-avatar')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
  
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling;
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈";
    } else {
        input.type = "password";
        icon.textContent = "👁️";
    }
}

(function () {
    document.addEventListener('DOMContentLoaded', function () {
      const searchInput = document.querySelector('.search-bar');
      const suggestionBox = document.querySelector('#suggestionBox');
  
      if (!searchInput || !suggestionBox) return;
  
      searchInput.addEventListener('input', function () {
        const query = this.value.trim();
  
        if (query.length < 2) {
          suggestionBox.innerHTML = '';
          return;
        }
  
        fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(data => {
            suggestionBox.innerHTML = '';
            data.suggestions.forEach(suggestion => {
              const li = document.createElement('li');
              li.textContent = suggestion;
              li.classList.add('suggestion-item');
              li.addEventListener('click', function () {
                searchInput.value = this.textContent;
                suggestionBox.innerHTML = '';
              });
              suggestionBox.appendChild(li);
            });
          })
          .catch(err => {
            console.error('Autocomplete fetch error:', err);
          });
      });
    });
  })();