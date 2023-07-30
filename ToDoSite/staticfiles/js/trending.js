document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('trendForm').addEventListener('submit', function(event) {
      event.preventDefault();

      const choiceValue = event.submitter.value;
  
      const formData = new FormData(this);
      formData.append('button', choiceValue);
  
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/topic/'); 
      xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken'));
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const responseData = JSON.parse(xhr.responseText);
    
                // Get the container where you want to display the tags
                const tagContainer = document.getElementsByClassName('categories')[0];
    
                // Clear the current content
                tagContainer.innerHTML = '';
    
                // Loop through the data and add the tags to the container
                responseData.categories.forEach(category => {
                    const tagElement = document.createElement('div');
                    tagElement.classList.add('category');
                    const tagButton = document.createElement('button');
                    const tagLink = document.createElement('a');
                    tagLink.href = `/topic/${category.tag}`;
                    tagLink.textContent = `${category.tag} (${category.post_count} posts)`;
                    tagButton.appendChild(tagLink);
                    tagElement.appendChild(tagButton);
                    tagContainer.appendChild(tagElement);
                });

                allTimeButton = document.getElementById("A");
                lastHourButton = document.getElementById("H");

                if (responseData.hour) {
                    allTimeButton.style.backgroundColor  = 'white';
                    lastHourButton.style.backgroundColor  = 'grey';
                  } else {
                    allTimeButton.style.backgroundColor  = 'grey';
                    lastHourButton.style.backgroundColor  = 'white';
                  }
    
                console.error('Success');
          } else {
            console.error('Request failed:', xhr.status);
          }
        }
      };
      
      xhr.send(formData);
    });
  });