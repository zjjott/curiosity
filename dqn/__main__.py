# coding=utf-8
from __future__ import unicode_literals, absolute_import
from dqn.history import History
import gym


def main():

    env = gym.make('CartPole-v0').unwrapped
    env.reset()
    screen = env.render(mode='rgb_array').transpose(
        (2, 0, 1))  # transpose into torch order (CHW)
    # Strip off the top and bottom of the screen
    screen = screen[:, 160:320]

    print("hello", screen.shape)


if __name__ == '__main__':
    main()
