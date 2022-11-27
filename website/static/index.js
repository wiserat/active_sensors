function deleteEmail(emailId) {
  fetch("/delete-email", {
    method: "POST",
    body: JSON.stringify({ emailId: emailId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
