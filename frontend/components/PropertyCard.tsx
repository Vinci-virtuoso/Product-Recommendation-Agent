import { Button } from "./ui/button";

interface Property {
  ProductId: number;
  ProductTitle: string;
  ImageURL: string;
  price: number;
}

interface PropertyCardProps {
  property: Property;
  isGridView?: boolean;
  isSaved?: boolean;
  toggleSavedProperty?: (property: Property) => void;
}

export default function PropertyCard({ property, isGridView = false, isSaved = false, toggleSavedProperty }: PropertyCardProps) {
  return (
    <div className={`bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden transition-transform transform hover:scale-105 ${isGridView ? 'cursor-pointer' : ''}`}>
      <div className="relative">
        <div className="h-40 bg-gray-700 flex items-center justify-center text-gray-300 text-lg">
          <img 
            src={property.ImageURL} 
            alt={property.ProductTitle}
            className="w-full h-full object-cover"
          />
        </div>
        <button 
          onClick={() => toggleSavedProperty?.(property)}
          className="absolute top-2 right-2 text-zinc-400 hover:text-red-500 transition-colors"
          aria-label={isSaved ? "Remove from saved" : "Save property"}
        >
          {isSaved ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 fill-red-500" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          )}
        </button>
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-white">{property.ProductTitle}</h3>
        <div className="flex justify-between text-sm text-gray-400">
          <span>Price:</span>
          <span className="font-bold">${property.price}</span>
        </div>
        <Button variant="ghost" className="mt-4 w-full text-gray-400 hover:bg-gray-700">
          View Details
        </Button>
      </div>
    </div>
  );
}
