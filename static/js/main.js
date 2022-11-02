// // for active nav
// var header = document.getElementById("index-nav");
// var btns = header.getElementsByClassName("nav1");
// for (var i = 0; i < btns.length; i++) {
// btns[i].addEventListener("click", function() {
// var current = document.getElementsByClassName("active");
// current[0].className = current[0].className.replace(" active", "");
// this.className += " active";
// });
// }


// $(document).ready(function() {
//     $('#myTable').DataTable( {
//         "pagingType": "full_numbers"
//     } );
// } );
const openButton = document.getElementById('deletebtn')
const modal =  document.querySelector('.bg-modal')
openButton.addEventListener('click', () => {
  modal.style.display ='flex'
})
const closeBtn =  document.querySelector('.close')
const modal =  document.querySelector('.bg-modal')
closeBtn.addEventListener('click', () => {
  modal.style.display ='none'
})


// delete popup
$('#delete_id').on('click',function(){
  $('#delete-confirm').modal('show');
 });


 $(document).ready(function(){
  $(".loader").fadeOut("slow");
 })