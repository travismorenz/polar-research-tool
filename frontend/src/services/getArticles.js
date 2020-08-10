export const getArticlesByProject = (selectedProjectId, page) =>
  fetch(`/articles-by-project/${selectedProjectId}?page=${page}`, {
    credentials: "include",
  }).then((res) => res.json());

export const getArticlesById = (ids) =>
  fetch("/articles-by-id", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ ids }),
  })
    .then((res) => res.json())
    .then(({ articles }) =>
      Object.values(articles).sort(
        (a, b) => new Date(a["publish_date"]) - new Date(b["publish_date"])
      )
    );
