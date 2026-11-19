export default function Logo({ size = 24, couleur = "#c62828" }) {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={couleur} aria-hidden="true">
        <path d="M12 2.5c3.2 4.2 6 7.4 6 11a6 6 0 0 1-12 0c0-3.6 2.8-6.8 6-11z" />
      </svg>
    );
  }