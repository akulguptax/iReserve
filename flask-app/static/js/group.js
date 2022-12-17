function join_group(event) {
  const group_id = event.currentTarget.group_id
  const url = "/join-group";
  const data = {
    'GroupID' : group_id
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
    
    if (response.status < 400) {
      console.log(response)
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("alert", "alert-success", "alert-dismissible", "fade", "show")
        msg.innerHTML = data.message;
      });
    } else {
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("alert", "alert-danger", "alert-dismissible", "fade", "show")
        msg.innerHTML = data.message;
      });
    }
  })
  .catch(err => {
    console.error(err.message);
    err.json().then((data) => {
      console.log(data);
      var msg = document.getElementById('message');
      msg.className = "";
      msg.classList.add("alert", "alert-danger", "alert-dismissible", "fade", "show")
      msg.innerHTML = data.message;
    });
  });

  return false;
}

var confirmModal = document.getElementById('confirmModal')
confirmModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var group_id = button.getAttribute('data-bs-gid')
  var group_name = button.getAttribute('data-bs-grp-name')
  var join_form = document.getElementById('join_group_form');
  join_form.group_id = group_id;

  var modalBodyMessage = confirmModal.querySelector('.modal-body p')
  modalBodyMessage.innerHTML = 'Are you sure you want to join the ' + group_name + '?'
})