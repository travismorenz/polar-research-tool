export default ({ projectId, article }) =>
  fetch(`/api/toggle-in-library/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ articleId: article.id }),
  });
