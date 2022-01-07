let balance = 200;

document.getElementById("balance").innerHTML = balance+"$";

let modal = document.querySelector(".modal");

let openBtn = document.querySelectorAll("[data-modal]");

let closeBtn = document.querySelector("[data-close]");

openBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        modal.style.display = "block"
    })
})

closeBtn.addEventListener('click', () => {
    modal.style.display = "none"
})

closeBtn.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

$(function() {
    $('input[name="daterange"]').daterangepicker({
        startDate: "01/10/2022",
        endDate: "01/01/2025",
        minDate: "01/15/2022",
        opens: 'right'
    }, function(start, end, label) {
      document.getElementById("totalPrice").innerHTML = `${(+end.format('D') - +start.format('D'))*30}$`;
    });
});

let confirm = document.getElementById("confirm")

confirm.onclick = function(){
    let totalPrice = document.getElementById("totalPrice").textContent;
    let temp = totalPrice.substring(0, totalPrice.length - 1);
    document.getElementById("balance").innerHTML = balance - +temp + "$";
    modal.style.display = "none";
}

