function try_to_make_reservation(event) {
  const room_id = event.currentTarget.room_id
  const url = "/reserve";
  const data = {
    'GroupID' : document.getElementById('groupid').value,
    'RoomID': room_id,
    'StartTime': document.getElementById('starttime').value
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
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("success", "alert", "alert-success")
        msg.innerHTML = data.message;
        document.getElementById('table-row-' + room_id).style.display = "none";
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

  window.scrollTo({ top: 0, behavior: 'smooth' });

  return false;
}

var confirmModal = document.getElementById('confirmModal')
confirmModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var rid = button.getAttribute('data-bs-roomid')
  var reserve_form = document.getElementById('make_res_form');
  reserve_form.room_id = rid;

  // var modalBodyMessage = confirmModal.querySelector('.modal-body p')
  // modalBodyMessage.innerHTML = 'Are you sure you want to delete your reservation in ' + building + ' Room ' + rnum + ' at ' + start_time + '?'
})