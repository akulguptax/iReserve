function update_name(event) {
  const url = "/users/update";
  const data = {
    'FirstName': document.getElementById('firstname').value,
    'LastName': document.getElementById('lastname').value,
  };

  console.log(data);

  fetch(url, {
    "method": "POST",
    "mode" : "cors",
    "headers": {
        "Content-Type": "application/json; charset=UTF-8"
    },
    "body": JSON.stringify(data)
  })
  .then(function(response) {
    console.log(response.url);
    response.json().then((data) => {
      console.log(data);
      document.getElementById('message').classList.add("primary")
      document.getElementById('message').innerHTML = data.message;
    });
  })
  .catch(err => {
    console.error(err.message);
    err.json().then((data) => {
      console.log(data);
      document.getElementById('message').classList.add("warning")
      document.getElementById('message').innerHTML = data.message;
    });
  });

  return false;
}