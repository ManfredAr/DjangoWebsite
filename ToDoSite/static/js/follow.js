document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('followForm').addEventListener('submit', function(event) {
      event.preventDefault();
  
      const formData = new FormData(this);
      s = document.getElementsByClassName("userId")[0].getAttribute("id");
      formData.append('person_id', s);
      console.log(formData.get('person_id'));
  
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/explore/follow-unfollow/'); 
      xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken'));
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            console.error('Success');
            location.reload();
          } else {
            console.error('Request failed:', xhr.status);
          }
        }
      };
      
      xhr.send(formData);
    });
  });