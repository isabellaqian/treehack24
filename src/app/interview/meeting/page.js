// buttons all hardcoded to direct to home page
import styles from "./page.module.css";
import Image from "next/image";
import Link from "next/link";
export default function Home() {
  return (
    <div className={styles.main}>
      <h1>Interview with AI Joe</h1>
      <div className={styles.convoWrapper}>
        <div className={styles.intvwrBlock}>
          <Image
            src="/interviewer_placeholder.png"
            width="76"
            height="66"
            alt="interviewer icon"
            className={styles.profile}
          />
          <div className={styles.intvwrText}>
            How do you think your experiences support your goal of becoming a
            full stack developer?
          </div>
        </div>
      </div>
      <div className={styles.videoWrapper}>
        <Image
          src="/interviewer_placeholder.png"
          width="537"
          height="323"
          alt="interviewer video"
          className={styles.video}
        />
        <Image
          src="/interviewer_placeholder.png"
          width="537"
          height="323"
          alt="interviewee video"
          className={styles.video}
        />
      </div>
      <div className={styles.icons}>
        <Link href="/">
          <Image
            src="/icons/microphone.svg"
            width="55"
            height="55"
            alt="microphone button"
          />
        </Link>
        <Link href="/">
          <Image
            src="/icons/video.svg"
            width="55"
            height="55"
            alt="video button"
          />
        </Link>
        <Link href="/">
          <Image
            src="/icons/share.svg"
            width="55"
            height="55"
            alt="sharing button"
          />
        </Link>
        <Link href="/">
          <Image
            src="/icons/more.svg"
            width="55"
            height="55"
            alt="more options button"
          />
        </Link>
        <Link href="/">
          <Image
            src="/icons/endcall.svg"
            width="55"
            height="55"
            alt="end call button"
          />
        </Link>
        <Link href="/">
          <Image
            src="/icons/info.png"
            width="35"
            height="35"
            alt="more info button"
          />
        </Link>
      </div>
    </div>
  );
}
