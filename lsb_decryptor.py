#!/usr/bin/env python3

import sys
import os
import argparse
from typing import Optional
from PIL import Image


def decode_lsb(image: Image.Image, bit_index: int = 0) -> str:
	"""Decode message from image using the LSB at the given bit index (0 = LSB, 3 = 4th bit).
	Stops at a null terminator (\x00) if present.
	"""
	if image.mode != 'RGB':
		image = image.convert('RGB')

	pixels = list(image.getdata())
	bits = []
	for pixel in pixels:
		for channel in pixel[:3]:
			bits.append(str((channel >> bit_index) & 1))

	# Assemble bits into bytes until null terminator
	message_chars = []
	for i in range(0, len(bits), 8):
		byte_bits = bits[i:i + 8]
		if len(byte_bits) < 8:
			break
		byte_val = int(''.join(byte_bits), 2)
		char = chr(byte_val)
		if char == '\x00':
			break
		message_chars.append(char)

	return ''.join(message_chars)


def try_decode(path: str) -> None:
	if not os.path.exists(path):
		print(f"[ERROR] File not found: {path}")
		return
	try:
		img = Image.open(path)
	except Exception as e:
		print(f"[ERROR] Could not open image '{path}': {e}")
		return

	print(f"\n=== Decoding: {path} ===")

	# Standard LSB (1st bit)
	try:
		msg_std = decode_lsb(img, bit_index=0)
		if msg_std.strip():
			print("[STANDARD LSB] Message:")
			print(msg_std)
		else:
			print("[STANDARD LSB] No message or empty.")
	except Exception as e:
		print(f"[STANDARD LSB] Error: {e}")

	# Crash variant (4th bit)
	try:
		msg_alt = decode_lsb(img, bit_index=3)
		if msg_alt.strip():
			print("[4TH-BIT LSB] Message:")
			print(msg_alt)
		else:
			print("[4TH-BIT LSB] No message or empty.")
	except Exception as e:
		print(f"[4TH-BIT LSB] Error: {e}")


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Standalone LSB image decryptor (standard 1st-bit and 4th-bit crash variant)",
	)
	parser.add_argument(
		"images",
		nargs='+',
		help="Path(s) to image files (PNG/JPG) to attempt decoding",
	)
	return parser.parse_args(argv)


def main() -> None:
	args = parse_args()
	for img_path in args.images:
		try_decode(img_path)


if __name__ == "__main__":
	main()
