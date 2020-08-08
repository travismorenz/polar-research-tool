export default (input) =>
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(input),
  }).then((res) => res.json());
