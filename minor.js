function verifyOTP() {
  const otp = document.getElementById("otp").value;
  const msg = document.getElementById("msg");

  if (otp === "") {
    msg.style.color = "red";
    msg.innerText = "Please enter the OTP";
  } else if (otp.length !== 6) {
    msg.style.color = "red";
    msg.innerText = "OTP must be 6 digits";
  } else {
    msg.style.color = "green";
    msg.innerText = "OTP Verified Successfully ✔";
  }
}

//OTP
function generateOtp(){
  let otp =""
  for(let i=0;i<4;i++){
  
  otp += Math.floor(Math.random()*6)}
  console.log(otp)
}
generateOtp()