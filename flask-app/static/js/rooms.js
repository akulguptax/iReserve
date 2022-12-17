function search_room(event) {
  const url = "/rooms";

  var searchParams = new URLSearchParams(window.location.search);
  searchParams.set("building", document.getElementById("search_bar").value);
  window.location.search = searchParams.toString();

  console.log(window.location.search);

  window.location.href = window.location.pathname + "?" + window.location.search;

  // var newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
  // history.pushState(null, '', newRelativePathQuery);
  return false;
}

// var button = document.getElementById("search_rooms_button");
// function handleForm(event) { event.preventDefault(); } 
// button.addEventListener('submit', handleForm);
