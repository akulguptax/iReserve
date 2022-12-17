function delete_reservation(event) {
    const rid = event.currentTarget.reservation_id
    const url = "/reservation/" + rid
    
    fetch(url, {
      "method": "DELETE",
      "mode" : "cors",
    })
    .then(function(response) {
      console.log(response.url);
      response.json().then((data) => {
        document.getElementById('message').classList.add("success", "alert", "alert-success")
        document.getElementById('message').innerHTML = data.message;
        document.getElementById('table-row-' + rid).style.display = "none";
      });
    })
    .catch(err => {
      console.error(err.message);
      err.json().then((data) => {
        console.log(data);
        document.getElementById('message').classList.add("warning", "alert", "alert-warning")
        document.getElementById('message').innerHTML = data.message;
      });
    });
  
    return false;
  }

var confirmModal = document.getElementById('confirmModal')
confirmModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var reservation_id = button.getAttribute('data-bs-rid')
  var rnum = button.getAttribute('meta-data-rnum')
  var building = button.getAttribute('meta-data-building')
  var start_time = button.getAttribute('meta-data-start')
  console.log(building)
  console.log(rnum)
  console.log(start_time)
  console.log(reservation_id)

  var delete_form = document.getElementById('delete_res_form');
  delete_form.reservation_id = reservation_id;

  var modalBodyMessage = confirmModal.querySelector('.modal-body p')
  modalBodyMessage.innerHTML = 'Are you sure you want to delete your reservation in ' + building + ' Room ' + rnum + ' at ' + start_time + '?'
})

function try_to_update_reservation(event) {
  const reservation_id = event.currentTarget.reservation_id
  const url = "/reservations";
  const data = {
    'GroupID' : document.getElementById('groupid').value,
    'ReservationID': reservation_id,
  };

  console.log(data);

  fetch(url, {
    "method": "PUT",
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
        document.getElementById('table-group-entry-' + reservation_id).innerHTML = data.new_group_name;
      });
    } else {
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("alert", "alert-warning", "alert-dismissible", "fade", "show")
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
      msg.classList.add("warning", "alert", "alert-warning")
      msg.innerHTML = data.message;
    });
  });

  return false;
}

var updateModal = document.getElementById('updateModal')
updateModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var reservation_id = button.getAttribute('data-bs-rid')
  var update_form = document.getElementById('update_res_form');
  update_form.reservation_id = reservation_id;
})