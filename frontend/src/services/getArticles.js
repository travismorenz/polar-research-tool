export default (selectedProjectId) =>
  fetch(`/articles/${selectedProjectId}`, {
    credentials: "include",
  })
    .then((res) => res.json())
    .then(({ articles, count }) => ({
      articles: Object.values(articles).sort(
        (a, b) => new Date(b["publish_date"] - new Date(a["publish_date"]))
      ),
      count,
    }));
