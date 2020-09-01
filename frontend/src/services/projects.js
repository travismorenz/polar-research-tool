export const addKeyphrase = (keyphrase, projectId) =>
  fetch(`/api/add-keyphrase/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ keyphrase }),
  }).then((res) => res.json());

export const removeKeyphrase = (keyphrase, projectId) =>
  fetch(`/api/remove-keyphrase/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ keyphrase }),
  }).then((res) => res.json());

export const addCategory = (category, projectId) =>
  fetch(`/api/add-category/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ category }),
  }).then((res) => res.json());

export const removeCategory = (category, projectId) =>
  fetch(`/api/remove-category/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ category }),
  }).then((res) => res.json());

export const getAllProjectNames = () =>
  fetch("/api/project-names").then((res) => res.json());

export const joinProject = (projectName) =>
  fetch(`/api/join-project`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ projectName }),
  }).then((res) => res.json());
