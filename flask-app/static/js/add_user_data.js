function add_user_data(event) {
    const url = "/register";
    const data = {
      'FirstName' : document.getElementById('first_name').value,
      'LastName' : document.getElementById('last_name').value,
      'Email' : document.getElementById('email').value,
      'HashedPassword' : document.getElementById('password').value,
    };
  
    console.log(data);
  
    fetch(url, {
      "method": "POST",
      "mode" : "cors",
      "redirect": "follow",
      "headers": {
          "Content-Type": "application/json; charset=UTF-8"
      },
      "body": JSON.stringify(data)
    })
    .then(function(response) {
      console.log(response.url);
      if (response.redirected) {
        window.location.href = response.url;
      } else if (response.status >= 400) {
        response.json().then((data) => {
          console.log(data);
          var msg = document.getElementById('message');
          msg.className = "";
          msg.classList.add("danger", "alert", "alert-danger")
          msg.innerHTML = data.message;
        });
      }
    })
    .catch(err => {
      console.error(err.message);
    });
  
    return false;
  }