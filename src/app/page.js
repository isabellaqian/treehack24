import Image from "next/image";
import styles from "./page.module.css";
import { roboto } from "./ui/fonts";
import Link from "next/link";

export default function Home() {
  return (
    <div className={styles.main}>
      <div
        className={styles.areYouReady}
      >{`Are you ready to ace your next job interview with confidence? Say hello to Ai&U – your personalized interview preparation assistant powered by cutting-edge artificial intelligence technology.`}</div>
      <div className={styles.frame}>
        <div className={styles.boostYourConfidenceContainer}>
          <p className={styles.boostYour}>Boost your</p>
          <p className={styles.boostYour}>{`confidence `}</p>
          <p className={styles.withAiu}>
            <span className={styles.with}>{`with `}</span>
            <span className={styles.aiu}>{`Ai&U`}</span>
          </p>
        </div>
        <div className={styles.experienceNowWrapper}>
          <Link href={"/interview"}>
            <div className={styles.experienceNow}>Experience Now</div>
          </Link>
        </div>
        <div className={styles.anAiPowered}>
          An AI powered platform to help you ace your interviews
        </div>
        <Image
          className={styles.image9Icon}
          src={"/landing2.png"}
          width="440"
          height="280"
        />
        <Image
          className={styles.image8Icon}
          src={"/landing1.png"}
          width="490"
          height="320"
        />
        {/* <img className={styles.image9Icon} alt="" src="/image-9@2x.png" />
        <img className={styles.image8Icon} alt="" src="/image-8@2x.png" /> */}
      </div>
    </div>
  );
}
