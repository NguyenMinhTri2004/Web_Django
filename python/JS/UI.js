// let mybutton = document.getElementById("return-btn");
// // When the user scrolls down 20px from the top of the document, show the button
// window.onscroll = function() {scrollFunction()};

// function scrollFunction() {
//   if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//     mybutton.style.display = "block";
//   } else {
//     mybutton.style.display = "none";
//   }
// }

// // When the user clicks on the button, scroll to the top of the document
// function topFunction() {
//   document.body.scrollTop = 0;
//   document.documentElement.scrollTop = 0;
// }

function OpenLogin(){
    document.getElementById('Login').style.display = "block";
    document.getElementById('Register').style.display = "none";
}

function OpenRegister(){
    document.getElementById('Register').style.display = "block";
    document.getElementById('Login').style.display = "none";
}

function ExitLog(){
    document.getElementById('Login').style.display = "none";
    document.getElementById('Register').style.display = "none";
}

// Tô lại màu ô nhập ở form đăng nhập
function ReprintLoginInputColor(){
  document.getElementById('txtUsernameLogin').style.borderColor = "black";
  document.getElementById('txtPasswordLogin').style.borderColor = "black";
}
// kiểm tra ô nhập trong form đăng nhập
function CheckLoginInput(){
  ReprintLoginInputColor();
  let Message = "";
    var Username = document.getElementById('txtUsernameLogin');
    var Password = document.getElementById('txtPasswordLogin');

  if (Username.value == "") {
    document.getElementById('txtUsernameLogin').style.borderColor = "red";
    Message += "- Tên người dùng không được bỏ trống!\n";
  }

  if (Password.value == "") {
    document.getElementById('txtPasswordLogin').style.borderColor = "red";
    Message += "- Mật khẩu không được bỏ trống!\n";
  }
  if (Message.length != 0)
    alert("Xin hãy kiểm tra các thông tin nhập sau đây: \n" + Message); 
}

// Tô lại màu ô nhập ở form đăng ký
function ReprintRegisterInputColor(){
  document.getElementById('txtUsernameRegister').style.borderColor = "black";
  document.getElementById('txtNumberPhoneRegister').style.borderColor = "black";
  document.getElementById('txtRePasswordRegister').style.borderColor = "black";
  document.getElementById('txtPasswordRegister').style.borderColor = "black";
  document.getElementById('txtEmailRegister').style.borderColor = "black";
}

// kiểm tra ô nhập trong form đăng ký
function CheckRegisterInput(){
  ReprintRegisterInputColor();
  let Message = "";
  
  var Vali_Numbers = /^[0-9]+$/;
  
  var Username = document.getElementById('txtUsernameRegister');
  var Number = document.getElementById('txtNumberPhoneRegister');
  var Email = document.getElementById('txtEmailRegister');
  var Password = document.getElementById('txtPasswordRegister');
  var RePassword = document.getElementById('txtRePasswordRegister');

  // kiểm tra tên người dùng
  if (Username.value == ""){
    document.getElementById('txtUsernameRegister').style.borderColor = "red";
    Message += "- Tên người dùng không được bỏ trống!\n";
  }

  // kiểm tra số điện thoại
  if (Number.value == ""){
    document.getElementById('txtNumberPhoneRegister').style.borderColor = "red";
    Message += "- Số điện thoại không được bỏ trống!\n";
  } else {
    // Số điện thoại buộc là số
    if (!Number.value.match(Vali_Numbers)){
      document.getElementById('txtNumberPhoneRegister').style.borderColor = "red";
      Message += "- Số điện thoại chỉ có số! \n";
    } else {
      // Số điện thoại đầu không phải 0
      if (Number.value.charAt(0) != "0"){
        document.getElementById('txtNumberPhoneRegister').style.borderColor = "red";
        Message += "- Ký tự đầu của số điện thoại phải là số 0 \n";
        } else {
        // Số điện thoại không quá 10 ký tự
        if (Number.value.length != 10){
          document.getElementById('txtNumberPhoneRegister').style.borderColor = "red";
          Message += "- Số điện thoại chỉ có 10 ký tự! \n";
        }
      } 
    }
  }

  // kiểm tra email
  if (Email.value == ""){
    document.getElementById('txtEmailRegister').style.borderColor = "red";
    Message += "- Email không được bỏ trống! \n";
  } else {
    let DotFlag = 0;
    let AtFlag = 0;
    for (let i = 0; i < Email.value.length ; i++ ){
      if (Email.value.charAt(i) == "@")
        AtFlag++;
      if (Email.value.charAt(i) == "." )
        DotFlag++;
    }
    if (DotFlag < 1 || AtFlag != 1){
      document.getElementById('txtEmailRegister').style.borderColor = "red";
      Message += "- Email không hợp lệ! \n";
    }
  }

  // Ô nhập mật khẩu
  if (Password.value == ""){
    document.getElementById('txtPasswordRegister').style.borderColor = "red";
    Message += "- Mật khẩu không được để trống! \n";
  } else {
    if (RePassword.value == ""){
      document.getElementById('txtRePasswordRegister').style.borderColor = "red";
      Message += "- Nhập lại mật khẩu không được để trống! \n";
    } else {
      if (!RePassword.value.match(Password.value)){
        document.getElementById('txtRePasswordRegister').style.borderColor = "red";
        Message += "- Mật khẩu phải trùng với mật khẩu trước đó! \n";
      }
    }
  } 

  if (Message.length != 0)
    alert("Xin hãy kiểm tra các thông tin nhập sau đây: \n" + Message); 
}

// Hiện mật khẩu
function HideShowPassword(myInput){
  var x = document.getElementById(myInput);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}



