import React from 'react';

const About: React.FC = () => {
  return (
    <section className="py-16 md:py-24 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-serif font-bold text-center mb-8">About Artisan Gems</h2>
        <div className="max-w-3xl mx-auto">
          <p className="text-gray-600 mb-6">
            Artisan Gems is a passion project born out of love for handcrafted jewelry. Our mission is to bring
            unique, high-quality pieces to jewelry enthusiasts who appreciate the artistry and craftsmanship
            behind each creation.
          </p>
          <p className="text-gray-600 mb-6">
            Every piece in our collection is carefully designed and handmade by skilled artisans, ensuring
            that each item is not just an accessory, but a work of art. We source ethically and use
            sustainable materials whenever possible, because we believe in creating beauty without
            compromising our values.
          </p>
          <p className="text-gray-600">
            When you choose Artisan Gems, you're not just buying jewelry – you're supporting a community
            of artists and embracing a piece of wearable art that tells a unique story.
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;