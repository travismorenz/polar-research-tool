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
