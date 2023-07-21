document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('.like-form');
    
    forms.forEach(function(form) {
      form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        var formId = form.id;
        // Get the form ID from the dataset attribute
        var formId = form.dataset.formId;

        // Get the clicked button's ID from the event object
        var buttonId = event.submitter.id;
        
        var likeButton = document.getElementById(buttonId);
        if (likeButton.classList.contains('disabled')) {
          return; // Prevent submitting the form again if the button is already disabled
        }

        likeButton.classList.add('disabled');

        const formData = new FormData(this);
        formData.append('form_id', formId);
        
        // Make an AJAX request
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/post/input-likes'); // Replace with your Django view URL
        xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken')); // Include the CSRF token
        xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              const responseData = JSON.parse(xhr.responseText);
              console.log(xhr.responseText)
              document.getElementById(responseData.id).innerHTML = responseData.like_count
              if (responseData.user_like == true) {
                document.getElementById(buttonId).style.color = "red";
              } else {
                document.getElementById(buttonId).style.color = "white";
              }
              likeButton.classList.remove('disabled');
            } else {
            // Handle an error response
              console.error('Request failed:', xhr.status);
              likeButton.classList.remove('disabled');
            }
        }
        };
        xhr.send(formData);
      });
    });
  });
  
  
  

