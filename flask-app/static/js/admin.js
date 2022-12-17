function call_stored_procedure(event) {
  console.log("running stored procedure...")
  const url = "/call-stored-procedure";
  const data = { };

  var btn = document.getElementById("stored-procedure-button")
  var btn_text = document.getElementById("stored-procedures-status-text")
  var btn_spinner = document.getElementById("stored-procedure-spinner")
  var indicator = document.getElementById("stored-procedure-success-indicator")
  
  btn.disabled = true;
  btn_text.innerHTML = "Loading...";
  btn_spinner.hidden = false;

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
    
    btn.disabled = false;
    btn_text.innerHTML = "Compute"
    btn_spinner.hidden = true;
    indicator.classList = []
    indicator.classList.add("badge", "rounded-pill", "bg-success")
    indicator.innerHTML = "Success"
    indicator.hidden = false;
  })
  .catch(err => {
    console.error("some error occurred");
    btn.disabled = false;
    btn_text.innerHTML = "Compute"
    btn_spinner.hidden = true;
    indicator.classList = []
    indicator.classList.add("badge", "rounded-pill", "bg-danger")
    indicator.innerHTML = "Error"
    indicator.hidden = false;
  });

  return false;
}
