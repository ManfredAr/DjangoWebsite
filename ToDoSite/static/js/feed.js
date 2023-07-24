document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('.like-form');
    
    forms.forEach(function(form) {
      form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        var formId = form.id;

        var formId = form.dataset.formId;


        var buttonId = event.submitter.id;
        
        var likeButton = document.getElementById(buttonId);
        if (likeButton.classList.contains('disabled')) {
          return; 
        }

        likeButton.classList.add('disabled');

        const formData = new FormData(this);
        formData.append('form_id', formId);
        
        // Make an AJAX request
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/post/input-likes'); 
        xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken'));
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
  
  
  
  document.addEventListener('DOMContentLoaded', function() {
    var commentButtons = document.querySelectorAll('.comment-button');
    var popup = document.getElementsByClassName("popup")[0];

    commentButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var postId = button.dataset.postId;
            var postContent = document.getElementById("p" + postId).textContent;
            document.getElementById('originID').innerHTML = postId;
            var popupContent = document.getElementById("PrevPost");
            popupContent.innerText = postContent;

            popup.style.display = 'block';
        });
    });
});



function remove() {
  document.getElementById("popup").style.display = "none";
}


document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('commentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    postId = document.getElementById('originID').innerHTML;
    formData.append('post_id', postId);
    console.log(formData);
  })
});


