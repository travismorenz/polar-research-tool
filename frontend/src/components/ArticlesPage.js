import React, { useState, useContext, useEffect } from "react";

import { AppContext } from "./App";

const ArticlesPage = () => {
  const [time, setTime] = useState("");
  const {
    state: { selectedProject },
    setState,
  } = useContext(AppContext);

  useEffect(() => {
    const init = async () => {
      const t1 = performance.now();
      const res = await fetch(
        `http://localhost:8080/articles/${selectedProject}`,
        {
          credentials: "include",
        }
      ).then((res) => res.json());
      console.log(res);
      console.log(Object.keys(res.articles).length);
      setTime(performance.now() - t1);
    };
    init();
  }, [selectedProject]);
  return (
    <div className="container grid-lg">
      <div className="space-between">
        <div className="tabs">
          <div className="btn-group btn-group-block" id="pagebar"></div>
        </div>
        <form id="search-bar" className="has-icon-left"></form>
      </div>
      {time}
    </div>
  );
};

export default ArticlesPage;
