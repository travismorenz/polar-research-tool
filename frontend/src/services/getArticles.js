export const getArticles = (_, projectId, page = 0) =>
  fetch(
    `/api/articles/${projectId === "_default" ? "" : projectId}?page=${page}`
  ).then((res) => res.json());

export const getLibrary = (_, projectId, page = 0) => {
  if (projectId === "_default") return;
  return fetch(`/api/articles/library/${projectId}?page=${page}`).then((res) =>
    res.json()
  );
};

export const getArticleIds = (projectId) =>
  fetch(
    `/api/article-ids/${projectId === "_default" ? "" : projectId}`
  ).then((res) => res.json());

export const getLibraryIds = (projectId) =>
  fetch(`/api/articles-by-library/${projectId}`).then((res) => res.json());

export const getArticlesById = (ids) =>
  fetch("/api/articles-by-id", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ids }),
  })
    .then((res) => res.json())
    .then(({ articles }) =>
      Object.values(articles).sort(
        (a, b) => new Date(a["publish_date"]) - new Date(b["publish_date"])
      )
    );
