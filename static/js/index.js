import * as THREE from 'https://cdn.skypack.dev/three@0.131.3';
import { Water } from 'https://cdn.skypack.dev/three@0.131.3/examples/jsm/objects/Water.js';

console.log(Water);

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

// Objects

// Water

const waterGeometry = new THREE.CircleGeometry(10000, 10000);

const water = new Water(waterGeometry, {
  textureWidth: 512,
  textureHeight: 512,
  waterNormals: new THREE.TextureLoader().load(
    "/static/img/waternormals.jpg",
    function (texture) {
      texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
    }
  ),
  sunDirection: new THREE.Vector3(),
  sunColor: new THREE.Color(0x959eac),
  waterColor: new THREE.Color(0x006994),
  fog: scene.fog !== undefined,
});

water.rotation.x = -Math.PI / 2;
water.position.x = -2.5;
water.position.y = 51;
water.position.z = -1710;

scene.add(water)

// Sun

const sunGeometry = new THREE.SphereGeometry(1000, 1000, 1000);
const sunMaterial = new THREE.MeshPhongMaterial({
  color: new THREE.Color(0xfce570),
  shininess: 100,
  transparent: true,
  opacity: 0.05,
});
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
sun.position.x = 500;
sun.position.y = 50;
sun.position.z = -10000;
scene.add(sun);

// Materials

// Mesh

// Lights

const light = new THREE.AmbientLight("#b68d5f", 1);
scene.add(light)

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 20000)
camera.position.x = 30
camera.position.y = 95
camera.position.z = 8300
scene.add(camera)

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    // alpha: true
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Animate
 */

const clock = new THREE.Clock()

const tick = () =>
{
    const elapsedTime = clock.getElapsedTime()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()