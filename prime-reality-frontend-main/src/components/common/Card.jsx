// reusable card component
// property card, section card aur dashboard card me reuse hoga

function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-[28px] shadow-lg border border-black/5 overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl ${className}`}
    >
      {children}
    </div>
  );
}

export default Card;