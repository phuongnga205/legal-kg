import React, { useEffect, useRef } from "react";
import { lawyers } from "../../data1/lawyers";
import "./LawyerList.css";

const LawyerList = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    console.log("Lawyers data:", lawyers); // 👈 Kiểm tra log
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, []);

  return (
    <div className="lawyer-list" ref={containerRef}>
      {lawyers.map((lawyer) => (
        <div key={lawyer.id} className="lawyer-card">
          <img src={lawyer.image} alt={lawyer.name} />
          <h3>{lawyer.name}</h3>
          <p>{lawyer.specialty}</p>
          <p>{lawyer.experience}</p>
        </div>
      ))}
    </div>
  );
};

export default LawyerList;