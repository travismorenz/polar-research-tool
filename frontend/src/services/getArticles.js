export default (selectedProject) =>
  fetch(`http://localhost:8080/articles/${selectedProject}`, {
    credentials: "include",
  })
    .then((res) => res.json())
    .then(({ articles }) =>
      Object.values(articles).sort(
        (a, b) => new Date(b["publish_date"] - new Date(a["publish_date"]))
      )
    );
