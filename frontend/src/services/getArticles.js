export const getArticleIds = (projectId) =>
  fetch(`/article-ids/${projectId === "_default" ? "" : projectId}`, {
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
