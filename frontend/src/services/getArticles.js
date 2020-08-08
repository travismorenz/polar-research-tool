export default (selectedProject) =>
  fetch(`/articles/${selectedProject}`, {
    credentials: "include",
  })
    .then((res) => res.json())
    .then(({ articles }) =>
      Object.values(articles).sort(
        (a, b) => new Date(b["publish_date"] - new Date(a["publish_date"]))
      )
    );
