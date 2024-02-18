"use client";
import { useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import { redirect } from "next/navigation";

export default function Home() {
  const [formData, setFormData] = useState({
    jobTitle: "",
    jobDescription: "",
    additionalDetails: "",
  });
  const [isVisible, setIsVisible] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    //MANUALLY redict to meeting page
    redirect("/interview/meeting");
    e.preventDefault(); // Prevent the default form submit action

    // Here you can handle the submission to your backend, for example:
    try {
      const response = await fetch("/api/submit-job", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        // Handle successful submission here
        alert("Job submitted successfully!");
        // Reset form or redirect user
        setFormData({
          jobTitle: "",
          jobDescription: "",
          additionalDetails: "",
        });
      } else {
        // Handle errors here
        alert("Submission failed.");
      }
    } catch (error) {
      console.error("Submission error:", error);
      alert("Submission error.");
    }
  };
  const submitForm = () => {
    document.getElementById("jobForm").submit();
  };
  return (
    <div className={styles.main}>
      <div className={styles.left}>
        <p style={{ "font-size": 32, "font-weight": 700 }}>
          Tell us about yourself.
        </p>
        <form onSubmit={handleSubmit} className={styles.form} id="jobForm">
          <div>
            <label htmlFor="jobTitle">Job Title</label>
            <br />
            <textarea
              type="text"
              id="jobTitle"
              name="jobTitle"
              value={formData.jobTitle}
              placeholder="Enter the job title"
              onChange={handleChange}
              className={styles.textarea}
            />
          </div>
          <div>
            <label htmlFor="jobDescription">Job Description</label>
            <br />
            <textarea
              id="jobDescription"
              name="jobDescription"
              value={formData.jobDescription}
              placeholder="Enter the job description, the company, location, and any other job related information."
              onChange={handleChange}
              className={styles.textarea}
            />
          </div>
          <div>
            <label htmlFor="additionalDetails">Additional Details</label>
            <br />
            <textarea
              id="additionalDetails"
              name="additionalDetails"
              value={formData.additionalDetails}
              placeholder="Enter any additional information."
              onChange={handleChange}
              className={styles.textarea}
            />
          </div>
          <div>
            <label htmlFor="chooseInterview">Choose your AI interviewer:</label>
          </div>
        </form>
      </div>
      <div className={styles.right}>
        <Image
          src="/interview.png"
          width="537"
          height="323"
          alt="interviewer"
        />
        <div className={styles.text}>
          Ready to embark on your journey to interview success? Click the button
          below to kickstart your interactive AI interview experience
        </div>
        <button onClick={submitForm} className={styles.button}>
          Begin interview
        </button>
        <div style={{ flexDirection: "row", display: "flex" }}>
          <input
            type="checkbox"
            id="toggleContent"
            checked={isVisible}
            onChange={(e) => setIsVisible(e.target.checked)}
          />
          <div>I understand my interview will be recorded</div>
        </div>
      </div>
    </div>
  );
}
