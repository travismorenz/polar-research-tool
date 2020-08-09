export default () =>
  fetch("/logout", {
    method: "POST",
    credentials: "include",
  });
