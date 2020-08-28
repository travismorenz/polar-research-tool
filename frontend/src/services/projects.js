export const addKeyphrase = (keyphrase, projectId) =>
  fetch(`/api/add-keyphrase/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ keyphrase }),
  }).then((res) => res.json());
