
import { ProductForm } from "@/components/ui/product-form"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center bg-black p-8">
      <h2 className="mb-8 text-xl font-semibold text-white">
        Product Recommendation and Ordering Agent
      </h2>
      <div className="w-full max-w-xl">
        <ProductForm />
      </div>
    </div>
  )
}
